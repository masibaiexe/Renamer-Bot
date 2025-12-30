import asyncio
import os
import time
from telethon import utils
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.functions.auth import ExportAuthorizationRequest
from telethon.tl.functions.upload import SaveBigFilePartRequest, GetFileRequest

# Define chunk size (Pyrogram uses 1MB or similar, we use 512KB aligned)
PART_SIZE_KB = 512
PART_SIZE = PART_SIZE_KB * 1024

async def fast_download(client, msg, file, progress_callback=None):
    """
    Downloads a file in parallel using multiple workers.
    """
    # Get the input location of the file
    media = msg.media
    if not media:
        raise ValueError("No media found in message")
    
    input_location = utils.get_input_location(media)
    if not input_location:
        raise ValueError("Could not get input location")

    # Get file size
    size = media.document.size if hasattr(media, 'document') else media.photo.sizes[-1].size
    
    # If file is small, use standard download
    if size < 10 * 1024 * 1024: # 10MB
        return await client.download_media(msg, file=file, progress_callback=progress_callback)

    # Open file for writing
    with open(file, 'wb') as f:
        f.truncate(size)

    # Calculate parts
    part_count = (size + PART_SIZE - 1) // PART_SIZE
    
    # Create a queue of parts to download
    queue = asyncio.Queue()
    for i in range(part_count):
        await queue.put(i)

    # Worker function
    async def worker():
        while not queue.empty():
            part_index = await queue.get()
            offset = part_index * PART_SIZE
            limit = PART_SIZE
            
            # Request chunk
            try:
                result = await client(GetFileRequest(
                    location=input_location,
                    offset=offset,
                    limit=limit
                ))
                
                # Write to specific location in file
                with open(file, 'r+b') as f:
                    f.seek(offset)
                    f.write(result.bytes)
                
                if progress_callback:
                    await progress_callback(min((part_index + 1) * limit, size), size)
                    
            except Exception as e:
                print(f"Part {part_index} failed: {e}")
                await queue.put(part_index) # Retry
            finally:
                queue.task_done()

    # Start workers (4 parallel connections is standard safe limit)
    workers = [asyncio.create_task(worker()) for _ in range(4)]
    await queue.join()
    
    for w in workers:
        w.cancel()
        
    return file

async def fast_upload(client, file_path, progress_callback=None, name=None):
    """
    Uploads a file in parallel. Returns the uploaded file object (InputFile).
    """
    file_size = os.path.getsize(file_path)
    
    # If small file, standard upload is fine
    if file_size < 10 * 1024 * 1024:
        return await client.upload_file(file_path, progress_callback=progress_callback)

    # Generate a unique file ID
    file_id = utils.generate_random_long()
    part_count = (file_size + PART_SIZE - 1) // PART_SIZE

    queue = asyncio.Queue()
    for i in range(part_count):
        await queue.put(i)

    async def worker():
        while not queue.empty():
            part_index = await queue.get()
            offset = part_index * PART_SIZE
            
            with open(file_path, 'rb') as f:
                f.seek(offset)
                data = f.read(PART_SIZE)
            
            try:
                await client(SaveBigFilePartRequest(
                    file_id=file_id,
                    file_part=part_index,
                    file_total_parts=part_count,
                    bytes=data
                ))
                
                if progress_callback:
                    await progress_callback(min((part_index + 1) * PART_SIZE, file_size), file_size)
                    
            except Exception as e:
                print(f"Upload Part {part_index} failed: {e}")
                await queue.put(part_index)
            finally:
                queue.task_done()

    # 4 Workers for upload
    workers = [asyncio.create_task(worker()) for _ in range(4)]
    await queue.join()
    
    for w in workers:
        w.cancel()

    # Return the handle
    from telethon.tl.types import InputFileBig
    return InputFileBig(
        id=file_id,
        parts=part_count,
        name=name if name else os.path.basename(file_path)
    )

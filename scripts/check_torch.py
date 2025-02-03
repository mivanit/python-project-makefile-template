import os
import sys
print(f'python version: {sys.version}')
print(f"\tpython executable path: {str(sys.executable)}")
print(f"\tsys_platform: {sys.platform}")
print(f'\tcurrent working directory: {os.getcwd()}')
print(f'\tHost name: {os.name}')
print(f'\tCPU count: {os.cpu_count()}')
print()

try:
	import torch
except Exception as e:
	print('ERROR: error importing torch, terminating        ')
	print('-'*50)
	raise e
	sys.exit(1)

print(f'torch version: {torch.__version__}')

print(f'\t{torch.cuda.is_available() = }')

if torch.cuda.is_available():
	# print('\tCUDA is available on torch')
	print(f'\tCUDA version via torch: {torch.version.cuda}')

	if torch.cuda.device_count() > 0:
		print(f"\tcurrent device: {torch.cuda.current_device() = }\n")
		n_devices: int = torch.cuda.device_count()
		print(f"detected {n_devices = }")
		for current_device in range(n_devices):
			try:
				# print(f'checking current device {current_device} of {torch.cuda.device_count()} devices')
				print(f'\tdevice {current_device}')
				dev_prop = torch.cuda.get_device_properties(torch.device(0))
				print(f'\t    name:                   {dev_prop.name}')
				print(f'\t    version:                {dev_prop.major}.{dev_prop.minor}')
				print(f'\t    total_memory:           {dev_prop.total_memory} ({dev_prop.total_memory:.1e})')
				print(f'\t    multi_processor_count:  {dev_prop.multi_processor_count}')
				print(f'\t    is_integrated:          {dev_prop.is_integrated}')
				print(f'\t    is_multi_gpu_board:     {dev_prop.is_multi_gpu_board}')
				print(f'\t')
			except Exception as e:
				print(f'Exception when trying to get properties of device {current_device}')
				raise e
		sys.exit(0)
	else:
		print(f'ERROR: {torch.cuda.device_count()} devices detected, invalid')
		print('-'*50)
		sys.exit(1)

else:
	print('ERROR: CUDA is NOT available, terminating')
	print('-'*50)
	sys.exit(1)
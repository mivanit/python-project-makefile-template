"print info about current python, torch, cuda, and devices"

from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def print_info_dict(
	info: Dict[str, Union[Any, Dict[str, Any]]],
	indent: str = "  ",
	level: int = 1,
) -> None:
	"pretty print the info"
	indent_str: str = indent * level
	longest_key_len: int = max(map(len, info.keys()))
	for key, value in info.items():
		if isinstance(value, dict):
			print(f"{indent_str}{key:<{longest_key_len}}:")
			print_info_dict(value, indent, level + 1)
		else:
			print(f"{indent_str}{key:<{longest_key_len}} = {value}")


def get_nvcc_info() -> Dict[str, str]:
	"get info about cuda from nvcc --version"
	# Run the nvcc command.
	try:
		result: subprocess.CompletedProcess[str] = subprocess.run(  # noqa: S603
			["nvcc", "--version"],  # noqa: S607
			check=True,
			capture_output=True,
			text=True,
		)
	except Exception as e:  # noqa: BLE001
		return {"Failed to run 'nvcc --version'": str(e)}

	output: str = result.stdout
	lines: List[str] = [line.strip() for line in output.splitlines() if line.strip()]

	# Ensure there are exactly 5 lines in the output.
	assert len(lines) == 5, (  # noqa: PLR2004
		f"Expected exactly 5 lines from nvcc --version, got {len(lines)} lines:\n{output}"
	)

	# Compile shared regex for release info.
	release_regex: re.Pattern = re.compile(
		r"Cuda compilation tools,\s*release\s*([^,]+),\s*(V.+)",
	)

	# Define a mapping for each desired field:
	# key -> (line index, regex pattern, group index, transformation function)
	patterns: Dict[str, Tuple[int, re.Pattern, int, Callable[[str], str]]] = {
		"build_time": (
			2,
			re.compile(r"Built on (.+)"),
			1,
			lambda s: s.replace("_", " "),
		),
		"release": (3, release_regex, 1, str.strip),
		"release_V": (3, release_regex, 2, str.strip),
		"build": (4, re.compile(r"Build (.+)"), 1, str.strip),
	}

	info: Dict[str, str] = {}
	for key, (line_index, pattern, group_index, transform) in patterns.items():
		match: Optional[re.Match] = pattern.search(lines[line_index])
		if not match:
			err_msg: str = (
				f"Unable to parse {key} from nvcc output: {lines[line_index]}"
			)
			raise ValueError(err_msg)
		info[key] = transform(match.group(group_index))

	info["release_short"] = info["release"].replace(".", "").strip()

	return info


def get_torch_info() -> Tuple[List[Exception], Dict[str, Any]]:
	"get info about pytorch and cuda devices"
	exceptions: List[Exception] = []
	info: Dict[str, Any] = {}

	try:
		import torch

		info["torch.__version__"] = torch.__version__
		info["torch.cuda.is_available()"] = torch.cuda.is_available()

		if torch.cuda.is_available():
			info["torch.version.cuda"] = torch.version.cuda
			info["torch.cuda.device_count()"] = torch.cuda.device_count()

			if torch.cuda.device_count() > 0:
				info["torch.cuda.current_device()"] = torch.cuda.current_device()
				n_devices: int = torch.cuda.device_count()
				info["n_devices"] = n_devices
				for current_device in range(n_devices):
					try:
						current_device_info: Dict[str, Union[str, int]] = {}

						dev_prop = torch.cuda.get_device_properties(
							torch.device(f"cuda:{current_device}"),
						)

						current_device_info["name"] = dev_prop.name
						current_device_info["version"] = (
							f"{dev_prop.major}.{dev_prop.minor}"
						)
						current_device_info["total_memory"] = (
							f"{dev_prop.total_memory} ({dev_prop.total_memory:.1e})"
						)
						current_device_info["multi_processor_count"] = (
							dev_prop.multi_processor_count
						)
						current_device_info["is_integrated"] = dev_prop.is_integrated
						current_device_info["is_multi_gpu_board"] = (
							dev_prop.is_multi_gpu_board
						)

						info[f"device cuda:{current_device}"] = current_device_info

					except Exception as e:  # noqa: PERF203,BLE001
						exceptions.append(e)
			else:
				err_msg_nodevice: str = (
					f"{torch.cuda.device_count() = } devices detected, invalid"
				)
				raise ValueError(err_msg_nodevice)  # noqa: TRY301

		else:
			err_msg_nocuda: str = (
				f"CUDA is NOT available in torch: {torch.cuda.is_available() = }"
			)
			raise ValueError(err_msg_nocuda)  # noqa: TRY301

	except Exception as e:  # noqa: BLE001
		exceptions.append(e)
		info["torch.__version__"] = "not available"

	return exceptions, info


if __name__ == "__main__":
	print(f"python: {sys.version}")
	print_info_dict(
		{
			"python executable path: sys.executable": str(sys.executable),
			"sys.platform": sys.platform,
			"current working directory: os.getcwd()": os.getcwd(),  # noqa: PTH109
			"Host name: os.name": os.name,
			"CPU count: os.cpu_count()": str(os.cpu_count()),
		},
	)

	nvcc_info: Dict[str, Any] = get_nvcc_info()
	print("nvcc:")
	print_info_dict(nvcc_info)

	torch_exceptions, torch_info = get_torch_info()
	print("torch:")
	print_info_dict(torch_info)

	if torch_exceptions:
		print("torch_exceptions:")
		for e in torch_exceptions:
			print(f"  {e}")

import os
import subprocess
import datetime
import itertools

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(ROOT_PATH, "in")
OUT_PATH = os.path.join(ROOT_PATH, "out")
BACKUP_PATH = os.path.join(ROOT_PATH, "backup")

SUFFIX = '.' + os.listdir(IN_PATH)[0].split(".")[1]


def rename_files():
	"""
	将包含中文名或特殊字符的文件名重命名。这样的视频不会被剪切。
	"""
	count = 0
	for filename in os.listdir(IN_PATH):
		if not all([ord(char) < 128 for char in filename]):
			os.rename(os.path.join(IN_PATH, filename), os.path.join(IN_PATH, str(count) + + SUFFIX))
			count += 1


def clip_videos():
	"""
	剪切视频。
	"""
	video_files = sorted([f for f in os.listdir(IN_PATH)])
	# 从原文件中提取出时间来。
	clip_files = [video for video in video_files if '@' in video]
	# print(clip_files)
	for video in clip_files:
		raw_name = video.split('@')[0] + SUFFIX
		if video.count('@') == 1:
			end_time = video.split('@')[1].split('.')[0].replace('_', ':')
			# print(end_time)
			clip_command = [os.path.join(ROOT_PATH, "ffmpeg.exe"),
							'-ss', '00:00:00',
							'-to', end_time,
							'-i', 'in/' + video,
							'-c', 'copy',
							'-avoid_negative_ts', '1',
							'in/' + raw_name]
		elif video.count('@') == 2:
			begin_time = video.split('@')[1].replace('_', ':')
			end_time = video.split('@')[2].split('.')[0].replace('_', ':')
			# print(begin_time, end_time)
			clip_command = [os.path.join(ROOT_PATH, "ffmpeg.exe"),
							'-ss', begin_time,
							'-to', end_time,
							'-i', 'in/' + video,
							'-c', 'copy',
							'-avoid_negative_ts', '1',
							'in/' + raw_name]
		# print(clip_command)
		subprocess.run(clip_command)
		try:
			os.rename(os.path.join(IN_PATH, video), os.path.join(BACKUP_PATH, video))
			print(f"视频{raw_name}剪切成功")
		except OSError as e:
			print(f"删除文件时发生错误: {e}")


def concat_videos():
	"""
	拼接视频。
	"""
	video_files = sorted([f for f in os.listdir(IN_PATH)])
	with open('in.txt', 'w') as file:
		for video in video_files:
			file.write(f"file \'in/{video}\'\n")
	output_name = 'out/' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_final") + SUFFIX
	concat_command = [
		os.path.join(ROOT_PATH, "ffmpeg.exe"),
		'-f', 'concat',
		'-safe', '0',
		'-i', 'in.txt',
		'-c', 'copy',
		output_name
	]
	subprocess.run(concat_command)

	print(f"视频已成功拼接，输出文件为： {output_name}")
	input("...")


if __name__ == '__main__':
	rename_files()
	clip_videos()
	concat_videos()

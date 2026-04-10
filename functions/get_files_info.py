import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        file_info = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            size = os.path.getsize(full_path)
            dir = os.path.isdir(full_path)
            file_info.append(f'- {item}: file_size={size} bytes, is_dir={dir}')
        return "\n".join(file_info)
    except Exception as e:
        return f"Error: {e}"
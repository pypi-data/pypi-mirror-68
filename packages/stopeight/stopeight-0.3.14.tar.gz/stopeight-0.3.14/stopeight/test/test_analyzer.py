def test_UserFiles():
    from stopeight.util.editor.modules import legacy
    from stopeight.util.editor.modules import file
    from stopeight.util.parser import process_directory
    from pathlib import Path
    lines = process_directory('.stopeight','.npy',file._read,legacy.stroke_sequential,base_dir=Path.home(),filename='UserFiles.out',drawResize=True)
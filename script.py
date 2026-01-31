import os
directories = [
    'templates',
    'static/css',
    'static/js',
    'static/images',
    'static/icons'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    
print("Directory structure created:")
for directory in directories:
    print(f"  {directory}/")
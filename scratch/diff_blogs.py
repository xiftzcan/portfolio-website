import difflib

with open('blog/digital-memory-blog.html', 'r', encoding='utf-8') as f:
    f1 = f.readlines()
with open('blog/essay/digital-memory-blog.html', 'r', encoding='utf-8') as f:
    f2 = f.readlines()

diff = difflib.unified_diff(f1, f2, fromfile='blog/digital-memory-blog.html', tofile='blog/essay/digital-memory-blog.html')
print(''.join(list(diff)[:30])) # Print first 30 lines of diff

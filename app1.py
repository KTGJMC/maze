import streamlit as st
import numpy as np
import random
from collections import deque

st.set_page_config(page_title="AI Navigator (Touch Mode)", layout="centered")

st.title("🧠 ตัวช่วย AI: เดินเขาวงกตด้วย BFS และ DFS")
st.markdown("เวอร์ชันสำหรับแท็บเล็ต: กดง่าย อ่านง่าย เรียนสนุก!")

# Layout improvements
st.markdown("### 🎯 เป้าหมาย: หาทางออกจากเขาวงกตโดยใช้ AI")

# Setup grid and obstacles
GRID_SIZE = st.slider("📏 ขนาดเขาวงกต (ช่อง)", 4, 10, 5)
maze = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
obstacles_count = st.slider("🚧 จำนวนสิ่งกีดขวาง", 0, GRID_SIZE * 2, GRID_SIZE)

# Generate obstacles randomly
for _ in range(obstacles_count):
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    maze[x][y] = 1

start = (0, 0)
goal = (GRID_SIZE - 1, GRID_SIZE - 1)
maze[start] = 0
maze[goal] = 0

# Display maze using emoji
def display_maze(maze, path=None):
    table = ""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) == start:
                cell = "🟢"
            elif (i, j) == goal:
                cell = "🏁"
            elif path and (i, j) in path:
                cell = "🟡"
            elif maze[i][j] == 1:
                cell = "⬛"
            else:
                cell = "⬜"
            table += cell
        table += "\n"
    st.markdown(f"<pre style='font-size: 24px'>{table}</pre>", unsafe_allow_html=True)

display_maze(maze)

# Search algorithms
def bfs(maze, start, goal):
    queue = deque([([start], start)])
    visited = set()
    while queue:
        path, (x, y) = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((path + [(nx, ny)], (nx, ny)))
    return []

def dfs(maze, start, goal):
    stack = [([start], start)]
    visited = set()
    while stack:
        path, (x, y) = stack.pop()
        if (x, y) == goal:
            return path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((path + [(nx, ny)], (nx, ny)))
    return []

# Radio buttons: big + spaced
algo = st.radio(
    "🤖 เลือกอัลกอริธึม AI", 
    ["🔄 ค้นกว้าง (BFS)", "🔁 ค้นลึก (DFS)"], 
    horizontal=True,
    index=0
)

# Big solve button
solve_button = st.button("🚀 เริ่มแก้เขาวงกต", use_container_width=True)

if solve_button:
    if "BFS" in algo:
        path = bfs(maze, start, goal)
    else:
        path = dfs(maze, start, goal)

    if path:
        st.success(f"✅ พบเส้นทางใน {len(path)-1} ก้าว")
        display_maze(maze, path)
    else:
        st.error("🚫 ไม่พบทางออก ลองเปลี่ยนวิธีหรือสิ่งกีดขวางให้น้อยลง")

# Sidebar for explanation
st.sidebar.markdown("## 📚 อธิบายแบบเข้าใจง่าย")
st.sidebar.markdown("""
### 🔄 BFS (ค้นกว้าง)
- สำรวจทุกทางก่อนลงลึก
- ได้ทางที่สั้นที่สุด
- เหมาะกับสถานการณ์ที่ต้องการทางเลือกที่ดีที่สุด

### 🔁 DFS (ค้นลึก)
- ลุยให้สุดทางก่อนค่อยย้อนกลับ
- เร็วกว่าแต่ไม่การันตีว่าทางที่ดีที่สุด

### 👩‍⚕️ เปรียบเทียบกับสถานการณ์ทางการแพทย์
- **BFS:** วางแผนดูผู้ป่วยทุกเคสก่อนลงมือ
- **DFS:** รับมือเคสฉุกเฉินโดยลุยเลย
""")

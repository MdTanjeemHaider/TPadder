import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.font as font

from PIL import Image, ImageFilter

def browseSource():
    path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    sourcePath.delete(0, tk.END) # Clear input
    sourcePath.insert(0, path) # Insert new path

def browseOutput():
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    outputPath.delete(0, tk.END) # Clear input
    outputPath.insert(0, path) # Insert new path

def initiate():
    result.config(text="Converting...")

    # Load source image
    sourceImg = Image.open(sourcePath.get())

    # Convert to tile texture 
    convert(sourceImg, outputPath.get())

    # Convert to tile texture highlight if needed
    if needHighlight.get() == 1:
        highlightedOutline = getHighlightedOutline(sourceImg)
        convert(highlightedOutline, outputPath.get()[:-4] + "_Highlighted.png")

    result.config(text="Complete!")
        
def convert(sourceImg, savePath):
    # Get the width and height of the image
    width, height = sourceImg.size

    # Calculate the number of blocks (1 block is 16x16 pixels)
    blockPerRow = width // 16
    blockPerColumn = height // 16

    # Create the result image with space between each block
    newWidth = width + (blockPerRow - 1) * 2
    newHeight = height + (blockPerColumn - 1) * 2
    resultImg = Image.new("RGBA", (newWidth, newHeight))

    # Paste each block into the result image with space between each block
    for row in range(blockPerRow):
        for col in range(blockPerColumn):
            # Calculate the position of the current block in the source image
            x = row * 16
            y = col * 16

            # Calculate the position of the current block in the result image
            newX = row * 18
            newY = col * 18

            # Crop the block from the source image
            block = sourceImg.crop((x, y, x + 16, y + 16))

            # Paste the block into the result image
            resultImg.paste(block, (newX, newY))
    
    # Save the result image
    resultImg.save(savePath)


def getHighlightedOutline(sourceImg):
    # Get the edges 
    outline = sourceImg.filter(ImageFilter.FIND_EDGES)

    # Highlight the outline in white
    for x in range(outline.width):
        for y in range(outline.height):
            # Extract the color of the current pixel
            r, g, b, a = outline.getpixel((x, y))

            if a == 255:
                # Set the color of the current pixel to white
                outline.putpixel((x, y), (255, 255, 255, 255))

    return outline

# Main window
window = tk.Tk()
window.iconbitmap("Icon/icon.ico")
window.title("TPadder")
window.geometry("350x250")

# Source section
tk.Label(window, text="Source Texture:", font=font.Font(weight="bold")).pack()
sourcePath = tk.Entry(window, width=50)
sourcePath.pack()
tk.Button(window, text="Browse", command=browseSource).pack()
# Output section
tk.Label(window, text="Output Texture:", font=font.Font(weight="bold")).pack()
outputPath = tk.Entry(window, width=50)
outputPath.pack()
tk.Button(window, text="Browse", command=browseOutput).pack()
# Start section
needHighlight = tk.IntVar()
tk.Checkbutton(window, text="Create highlight texture", variable=needHighlight).pack()
tk.Button(window, text="Start", command=initiate).pack()
# Result section
tk.Label(window, text="Result:", font=font.Font(weight="bold")).pack()
result = tk.Label(window, text="Waiting for input...")
result.pack()

window.mainloop()
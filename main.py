import numpy as np
import math

class Suduko:
    
    def __init__(self,frames):
        self.frames = frames
    
    def defaultOpts(self):
        optFrames = []
        for n in range(9):
            opts = []
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    el = self.grid[row,colm]
                    
                    if frameInd == n:
                        if el != 0:
                            opts.append([el])
                        else:
                            r = self.rows[row]
                            c = self.colms[colm]
                            b = self.frames[frameInd]
                        
                            opt = [m for m in range(1,10) if m not in r and m not in c and m not in b]
                            opts.append(opt)
            
            optFrames.append(opts)
        
        self.optFrames = optFrames
        
    def commonOpts(self):
        [self.gridOpts,self.rowOpts,self.colmOpts] = gridMat(self.optFrames)
        
        
        gridOpts = []
        for n in range(9):
            frameOpts = []
            ind = 0
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    if frameInd == n:
                        frameOpts.append(opts[ind])
                        
                    ind += 1
                    
            gridOpts.append(frameOpts)
        
        for frame in gridOpts:
            frameOpts = [opt for el in frame for opt in el]
            
            for el in frame:
                try:            
                    if len(el) == 1:
                        self.grid[row,colm] = self.opts[ind][0]
                        defCheck = True
                        
                        print((row,colm,self.grid[row,colm]))
                except:
                    pass
#                if frameOpts.count(n) = 1
            
        self.opts = gridOpts
    
    def frameMat(self):
        frames = []
        for n in range(9):
            frame = []
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    if frameInd == n:
                        frame.append(self.grid[row,colm])
            
            frames.append(frame)
                        
        self.frames = frames
    
    def solve(self):
        defCheck = False
        while True:
            self.optsMat()
            
            ind = 0
            for row in range(9):
                for colm in range(9):
                    try:            
                        if len(self.opts[ind]) == 1:
                            self.grid[row,colm] = self.opts[ind][0]
                            defCheck = True
                            
                            print((row,colm,self.grid[row,colm]))
                    except:
                        pass
                    
                    ind += 1
                    
            self.frameMat()
            
            self.rowMat()
            self.colmMat()
            
            self.gridMat()

            if not defCheck:
                break
    
    def run(self):
        [self.grid,self.rows,self.colms] = gridMat(self.frames)
        inGrid = self.grid
        
        self.defaultOpts()
        [self.gridOpts,self.rowOpts,self.colmOpts] = gridMat(self.optFrames)
        
#        self.solve()
#        self.optsMat()
        
        return [self.gridOpts,self.rowOpts,self.colmOpts]


def gridMat(frames):
    def rowMat():
        rows = []
        for n in range(3):
            for m in range(3):
                rowFrame = frames[n*3:(n*3)+3]
                
                row = []
                for frame in rowFrame:
                    row.extend(frame[m*3:(m*3)+3])
                
                rows.append(row)
                
        return rows
    
    def colmMat():
        colms = []
        for n in range(3):
            for m in range(3):
                colmFrame = [frames[x] for x in range(n,9,3)]
                
                colm = []
                for frame in colmFrame:
                    colm.extend([frame[x] for x in range(m,9,3)])
                
                colms.append(colm)
                
        return colms
    
    rows = rowMat()
    colms = colmMat()
    
    grid = np.array(colms).transpose()
    
    return [grid,rows,colms]

frames = [[3,0,4,1,8,0,0,0,0],[0,7,0,0,6,0,1,3,0],[0,0,9,0,3,7,8,0,0],
          [8,3,0,5,0,0,0,0,0],[0,0,0,0,2,8,0,4,0],[7,0,5,0,9,0,0,0,3],
          [0,0,0,0,0,0,0,0,0],[0,5,0,0,9,0,6,0,0],[9,7,6,0,5,0,0,0,0]]

suduko = Suduko(frames)
[grid,row,colm] = suduko.run()
    
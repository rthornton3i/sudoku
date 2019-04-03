import numpy as np
import math

class Suduko:
    
    def __init__(self,frames):
        self.frames = frames
    
    def singleOpts(self):
        optFrames = []
        for n in range(9):
            opts = []
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    
                    el = self.rows[row][colm]
                    
                    if frameInd == n:
                        if el != 0:
                            opts.append([el])
                        else:
                            r = self.rows[row]
                            c = self.colms[colm]
                            f = self.frames[frameInd]
                        
                            opt = [m for m in range(1,10) if m not in r and m not in c and m not in f]
                            opts.append(opt)
            
            optFrames.append(opts)
        
        self.optFrames = optFrames
        
    def hidSingleOpts(self):
        [_,_,rowOpts,colmOpts] = gridMat(frames=self.optFrames)
        
        optFrames = []
        for n in range(9):
            opts = []
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    optsFrame = [opt for elOpt in self.optFrames[frameInd] for opt in elOpt]
                    optsRow = [opt for elOpt in rowOpts[row] for opt in elOpt]
                    optsColm = [opt for elOpt in colmOpts[colm] for opt in elOpt]
                    
                    elOpts = rowOpts[row][colm]
                    
                    if frameInd == n:
                        if len(elOpts) == 1:
                            opts.append(elOpts)
                        else:
                            uniqueCheck = False
                            for m in elOpts:
                                if optsFrame.count(m) == 1 or optsRow.count(m) == 1 or optsColm.count(m) == 1:
                                    uniqueCheck = True
                                    break
                            
                            if uniqueCheck:
                                opts.append([m])
                            else:
                                opts.append(elOpts)
            
            optFrames.append(opts)
            
        self.optFrames = optFrames
    
    def solve(self):
        def singleSolve():
            while True:
                tempGrid = np.copy(self.grid)
                
                self.singleOpts()
                [_,_,rowOpts,_] = gridMat(frames=self.optFrames)
                
                for row in range(9):
                    for colm in range(9):
                        if len(rowOpts[row][colm]) == 1:
                            self.grid[row,colm] = rowOpts[row][colm][0]
    #                        print((row,colm,rowOpts[row][colm][0]))
                            
                [self.frames,_,self.rows,self.colms] = gridMat(grid=self.grid)
                        
                if np.sum(tempGrid - self.grid) == 0:
                    break      
        
        def hidSingleSolve():
            while True:
                tempGrid = np.copy(self.grid)
                
                self.hidSingleOpts()
                [_,_,rowOpts,_] = gridMat(frames=self.optFrames)
                
                for row in range(9):
                    for colm in range(9):
                        if len(rowOpts[row][colm]) == 1:
                            self.grid[row,colm] = rowOpts[row][colm][0]
    #                        print((row,colm,rowOpts[row][colm][0]))
                            
                [self.frames,_,self.rows,self.colms] = gridMat(grid=self.grid)
                        
                if np.sum(tempGrid - self.grid) == 0:
                    break
                
        while True:
            tempGrid = np.copy(self.grid)
            
            singleSolve()
            hidSingleSolve()
            
            if np.sum(tempGrid - self.grid) == 0:
                break        
    
    def guess(self):
        grid = np.copy(self.grid)
        [_,_,rowOpts,_] = gridMat(frames=self.optFrames)
        
        n = 1
        while True:
            if n % 1000 == 0:
                print('Loop: ' + str(n))
            
            for row in range(9):
                for colm in range(9):
                    if grid[row,colm] == 0:
                        grid[row,colm] = rowOpts[row][colm][np.random.randint(len(rowOpts[row][colm]))]
            
            [self.frames,_,self.rows,self.colms] = gridMat(grid=grid)
            self.check()
            
            if self.gridCheck is False:
                grid = np.copy(self.grid)
            else:
                break
            
            n += 1
            
    def check(self):
        gridCheck = True
        if gridCheck:
            for frame in self.frames:
                for n in range(1,10):
                    if frame.count(n) != 1:
                        gridCheck = False
                        break
                
                if gridCheck is False:
                    break
        
        if gridCheck:
            for row in self.rows:
                for n in range(1,10):
                    if row.count(n) != 1:
                        gridCheck = False
                        break
                
                if gridCheck is False:
                    break
        
        if gridCheck:
            for colm in self.colms:
                for n in range(1,10):
                    if colm.count(n) != 1:
                        gridCheck = False
                        break
                
                if gridCheck is False:
                    break
            
        self.gridCheck = gridCheck
    
    def run(self):
        [_,self.grid,self.rows,self.colms] = gridMat(frames=self.frames)
        inGrid = np.copy(self.grid)
       
        self.solve()
        self.check()
        
        if self.gridCheck is False:
            self.guess()
        
        return [inGrid,self.grid,self.optFrames]

#==============================================================================

def gridMat(frames=None,grid=None):
    def frameMat():
        frames = []
        for n in range(9):
            frame = []
            for row in range(9):
                for colm in range(9):
                    frameInd = math.floor(row/3)*3 + math.floor(colm/3)
                    if frameInd == n:
                        frame.append(grid[row,colm])
            
            frames.append(frame)
        
        return frames
        
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
    
    def gridSet():
        grid = np.zeros((9,9))
        rowInd = 0
        for row in rows:
            colmInd = 0
            for colm in row:
                if type(colm) is int:
                    grid[rowInd,colmInd] = colm
                elif type(colm) is list:
                    grid[rowInd,colmInd] = colm[0] if len(colm) == 1 else 0
                    
                colmInd += 1
                    
            rowInd += 1
                         
        return grid
    
    if frames is None:
        frames = frameMat()
        
    rows = rowMat()
    colms = colmMat()
    
    grid = gridSet()
    
    return [frames,grid,rows,colms]

#==============================================================================

frames = [[3,0,4,1,8,0,0,0,0],[0,7,0,0,6,0,1,3,0],[0,0,9,0,3,7,8,0,0],
          [8,3,0,5,0,0,0,0,0],[0,0,0,0,2,8,0,4,0],[7,0,5,0,9,0,0,0,3],
          [0,0,0,0,0,0,0,0,0],[0,5,0,0,9,0,6,0,0],[9,7,6,0,5,0,0,0,0]]

suduko = Suduko(frames)
[inGrid,outGrid,optFrames] = suduko.run()    
from scipy.spatial import Delaunay, delaunay_plot_2d
import numpy as np
#import meshio
import dmsh
#import optimesh
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler()) # Add other handlers if you're using this as a library
logger.setLevel(logging.INFO)


def radius(k,n,b):
    if k>n-b:
        r = 1            # put on the boundary
    else:
        r = np.sqrt(k+1/2)/np.sqrt(n-(b+1)/2)     # apply square root
    return r

def sunflower(n, rad, alpha):   #  example: n=500, alpha=2

    b = np.round(alpha*np.sqrt(n))      # number of boundary points
    phi = (np.sqrt(5)+1)/2           # golden ratio
    phi2 = phi**2
    
    ret = []
    for k in range(n):
        r = radius(k,n,b)*rad
        theta = 2*np.pi*k/phi2
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        ret.append([x,y])
        
    return np.array(ret)



class UnstructuredMesh:
    
    def __init__(self, N, radius):
        
        geo = dmsh.Circle([0.0, 0.0], radius)

        logger.info("Generating Mesh")
        res = np.sqrt(2*np.pi*radius*radius / N)
        X, cells = dmsh.generate(geo, res, tol=res/100)
        logger.info(" Mesh generated {}".format(cells.shape))
        
        logger.info("Optimizing Mesh")
        X, cells = optimesh.odt.fixed_point_uniform(X, cells, 1e-2, 100, verbose=True)

        self.pts = X
        #self.pts = sunflower(N, radius, alpha=2)
        self.tri = Delaunay(self.pts, incremental=True)
        self.mesh()
        
    def mesh(self):
        self.npix = self.tri.simplices.shape[0]
        logger.info("New Mesh {}".format(self.npix))
        self.pixels = np.zeros(self.npix)
        self.centroids = np.sum(self.tri.points[self.tri.simplices], axis=1)/3

    def optimize(self):
        logger.info("Optimizing Mesh")
        X, cells = optimesh.odt.fixed_point_uniform(self.pts, self.tri.simplices, 1e-2, 100, verbose=True)
        self.pts = X
        #self.pts = sunflower(N, radius, alpha=2)
        self.tri = Delaunay(self.pts, incremental=True)
        self.mesh()



    def plot(self):
        import matplotlib.pyplot as plt
        #plt.plot(pts[:,0], pts[:,1], '.')
        plt.plot(self.tri.points[:,0], self.tri.points[:,1], 'o')
        plt.plot(self.centroids[:,0], self.centroids[:,1], '.')
        plt.triplot(self.tri.points[:,0], self.tri.points[:,1], self.tri.simplices.copy())
        plt.show()

    def gradient(self):
        # Return a gradient between every pair of cells
        ret = []
        cell_pairs = []
        for p1, nlist in enumerate(self.tri.neighbors):
            y1 = self.pixels[p1]
            #print(p1, nlist)
            for p2 in nlist:
                if p2 != -1:
                    dx, dy = self.centroids[p2] - self.centroids[p1]
                    r = np.sqrt(dx*dx + dy*dy)
                    grad = (y1 - self.pixels[p2])/r
                    ret.append(grad)
                    cell_pairs.append([p1, p2])
        return np.array(ret), cell_pairs
    
    
    def refine(self):
        grad, pairs = self.gradient()

        self.refine_adding(grad, pairs)
        
    def refine_adding(self, grad, pairs):
        
        p05, p50, p95 = np.percentile(np.abs(grad), [5, 50, 95])
        print("Data {} {} {}".format(p05, p50, p95))

        new_pts = []
        for g, p in zip(grad, pairs):
            #print(g, p)
            if (g > p95):
                pt = (self.centroids[p[0]] + self.centroids[p[1]])/ 2
                new_pts.append(pt)
                print("adding point {}".format(pt))

        self.tri.add_points(new_pts)
        #self.optimize()
        self.mesh()
        
    def refine_removing(self, grad, pairs):

        grad, pairs = self.gradient()
        p05, p50, p95 = np.percentile(np.abs(grad), [5, 50, 95])
        print("Data {} {} {}".format(p05, p50, p95))

        # Go through points and find the max gradient between all cells that contain that point.
        # If below a threshold, remove the point
        indices, indptr = self.tri.vertex_neighbor_vertices()
        # The indices of neighboring vertices of vertex k are indptr[indices[k]:indices[k+1]].
        
        

        
    def write_mesh(self, fname='output.vtk'):
        #import matplotlib.pyplot as plt
        
        #plt.plot(self.l, self.m, 'x')
        ###plt.plot(el_r, az_r, 'x')
        #plt.show()

        # and write it to a file
        meshio.write_points_cells(fname, self.tri.points, {"triangle": self.tri.simplices}, 
                                  cell_data={'triangle': {'flux': self.pixels}})

if __name__=="__main__":
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('disko.log')
    fh.setLevel(logging.INFO)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)


    um = UnstructuredMesh(400, 0.2)
    #for i in range(5):
        #um.pixels = np.random.random(um.npix)
        #um.refine()
    um.write_mesh('new.vtk')
    um.plot()



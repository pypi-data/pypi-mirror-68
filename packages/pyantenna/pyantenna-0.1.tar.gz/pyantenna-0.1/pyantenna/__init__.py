class MicrostripAntenna:

    def __init__(self):
        print("Welcome")

    def calculateDimensionRectangular(self, dicon, fr, h):
        
        W = (3*10e8/2*fr)*((2/(dicon+1)**0.5))
        dicon_effective = (dicon+1)/2 + (dicon-1)/2 * ((1+12*(h/W))**(-0.5))

        delL= (h * 0.412 * (dicon_effective + 0.3)*(W/h + 0.264))/((dicon_effective-0.258)/(W/h+0.8))

        L = 3*10e8/(2*fr*(dicon_effective ** 0.5)) - 2*delL

        return L,W



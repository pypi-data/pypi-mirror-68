import CADETMatch.util as util
import numpy
from CADETMatch.abstract.transform import AbstractTransform

class NuSigmaTransform(AbstractTransform):
    @property
    def name(self):
        return "nu_sigma"

    @property
    def count(self):
        return 2

    @property
    def count_extended(self):
        return 3

    def transform(self):
        def trans_a(i):
            return i

        def trans_b(i):
            return i

        return [trans_a, trans_b]

    grad_transform = transform

    def untransform(self, seq):
        values = [seq[0], seq[1] - seq[0]]
        headerValues = [values[0], values[1], values[0]+values[1]]
        return values, headerValues

    def grad_untransform(self, seq):
        return self.untransform(seq)[0]

    def untransform_matrix(self, matrix):
        values = self.untransform_matrix_inputorder(matrix)
        values[:,1] = matrix[:,1] - matrix[:,0]
        return values

    def untransform_matrix_inputorder(self, matrix):
        values = numpy.zeros(matrix.shape)
        values[:,1] = matrix[:,1]
        values[:,0] = matrix[:,0]
        return values

    def setSimulation(self, sim, seq, experiment):
        values, headerValues = self.untransform(seq)
    
        if self.parameter.get('experiments', None) is None or experiment['name'] in self.parameter['experiments']:
            nu_location = self.parameter['nu_location']
            sigma_location = self.parameter['sigma_location']
    
            comp = self.parameter['component']
            bound = self.parameter['bound']
    
            unit = self.getUnit(nu_location)
            boundOffset = util.getBoundOffset(sim.root.input.model[unit])

            position = boundOffset[comp] + bound
            sim[nu_location.lower()][position] = values[0]
            sim[sigma_location.lower()][position] = values[1]

        return values, headerValues

    def setupTarget(self):
        nu_location = self.parameter['nu_location']
        sigma_location = self.parameter['sigma_location']
        bound = self.parameter['bound']
        comp = self.parameter['component']

        sensitivityOk = 1
        nameNu = nu_location.rsplit('/', 1)[-1]
        nameSigma = sigma_location.rsplit('/', 1)[-1]
        unit = int(nu_location.split('/')[3].replace('unit_', ''))

        return [(nameNu, unit, comp, bound), (nameSigma, unit, comp, bound)], sensitivityOk

    def getBounds(self):
        minNu = self.parameter['minNu']
        maxNu = self.parameter['maxNu']
        minSigma = self.parameter['minSigma']
        maxSigma = self.parameter['maxSigma']

        minValues = [minNu, minNu+minSigma]
        maxValues = [maxNu, maxNu+maxSigma]

        return minValues, maxValues

    def getGradBounds(self):
        return [self.parameter['min'],], [self.parameter['max'],]

    def getHeaders(self):
        nu_location = self.parameter['nu_location']
        sigma_location = self.parameter['sigma_location']
        nameNu = nu_location.rsplit('/', 1)[-1]
        nameSigma = sigma_location.rsplit('/', 1)[-1]
        bound = self.parameter['bound']
        comp = self.parameter['component']
    
        headers = []
        headers.append("%s Comp:%s Bound:%s" % (nameNu, comp, bound))
        headers.append("%s Comp:%s Bound:%s" % (nameSigma, comp, bound))
        headers.append("%s+%s Comp:%s Bound:%s" % (nameNu, nameSigma, comp, bound))
        return headers

    def getHeadersActual(self):
        nu_location = self.parameter['nu_location']
        sigma_location = self.parameter['sigma_location']
        nameNu = nu_location.rsplit('/', 1)[-1]
        nameSigma = sigma_location.rsplit('/', 1)[-1]
        bound = self.parameter['bound']
        comp = self.parameter['component']
    
        headers = []
        headers.append("%s Comp:%s Bound:%s" % (nameNu, comp, bound))
        headers.append("%s+%s Comp:%s Bound:%s" % (nameNu, nameSigma, comp, bound))
        return headers

    def setBounds(self, parameter, lb, ub):
        parameter['minNu'] = lb[0]
        parameter['maxNu'] = ub[0]
        parameter['minSigma'] = lb[1]
        parameter['maxSigma'] = ub[1]

class NormNuSigmaTransform(NuSigmaTransform):
    @property
    def name(self):
        return "norm_nu_sigma"

    def transform(self):
        minNu = self.parameter['minNu']
        maxNu = self.parameter['maxNu']
        minSigma = self.parameter['minSigma']
        maxSigma = self.parameter['maxSigma']

        def trans_a(i):
            return (i - minNu)/(maxNu-minNu)

        def trans_b(i):
            return (i - minSigma)/(maxSigma-minSigma)

        return [trans_a, trans_b]

    grad_transform = transform

    def untransform(self, seq):
        minNu = self.parameter['minNu']
        maxNu = self.parameter['maxNu']
        minSigma = self.parameter['minSigma']
        maxSigma = self.parameter['maxSigma']

        minValues = numpy.array([minNu, minNu+minSigma])
        maxValues = numpy.array([maxNu, maxNu+maxSigma])

        values = numpy.array(seq)

        values = (maxValues - minValues) * values + minValues

        values = [values[0], values[1] - values[0]]
        headerValues = [values[0], values[1], values[0]+values[1]]
        return values, headerValues

    def grad_untransform(self, seq):
        return self.untransform(seq)[0]

    def untransform_matrix(self, matrix):
        values = self.untransform_matrix_inputorder(matrix)
        values[:,1] = values[:,1] - values[:,0]
        return values

    def untransform_matrix_inputorder(self, matrix):
        minNu = self.parameter['minNu']
        maxNu = self.parameter['maxNu']
        minSigma = self.parameter['minSigma']
        maxSigma = self.parameter['maxSigma']

        minValues = numpy.array([minNu, minNu+minSigma])
        maxValues = numpy.array([maxNu, maxNu+maxSigma])

        temp = (maxValues - minValues) * matrix + minValues

        values = numpy.zeros(temp.shape)
        values[:,0] = temp[:,0]
        values[:,1] = temp[:,1]

        return values

    def getBounds(self):
        return [0.0, 0.0], [1.0, 1.0]

    def getGradBounds(self):
        return [self.parameter['min'],], [self.parameter['max'],]

plugins = {"nu_sigma": NuSigmaTransform, "norm_nu_sigma": NormNuSigmaTransform}   
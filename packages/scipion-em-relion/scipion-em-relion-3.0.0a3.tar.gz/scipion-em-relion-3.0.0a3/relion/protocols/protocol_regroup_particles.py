# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology, MRC-LMB
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from math import log, floor

from pyworkflow.protocol.params import PointerParam, IntParam
from pyworkflow.object import String, Integer

import relion.convert as convert
from relion.convert.metadata import Table
from .protocol_base import ProtRelionBase

 
class ProtRelionRegroupParts(ProtRelionBase):
    """ This protocols regroups particles after a Relion run.

    Given an input set of particles after Refine3D or
    classification job, new groups are assigned based on
    intensity scale.
    """
    _label = 'regroup particles'

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputProt', PointerParam,
                      important=True,
                      pointerClass='ProtRelionRefine3D,ProtRelionClassify3D,'
                                   'ProtRelionClassify2D',
                      label="Input Relion protocol")
        form.addParam('nrGroups', IntParam, default=1,
                      label='Approx number of groups',
                      help='The program will regroup the output '
                           'particles in *more-or-less* the number '
                           'of groups provided here.')
        form.addParallelSection(threads=0, mpi=0)

    # -------------------------- INSERT steps functions -----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('regroupStep')
        self._insertFunctionStep('createOutputStep')

    # -------------------------- STEPS functions ------------------------------
    def regroupStep(self):
        prot = self.inputProt.get()
        prot._initialize()
        fnModel = prot._getFileName('modelFinal')
        fnData = prot._getFileName('dataFinal')
        fnOut = self._getExtraPath("particles_regrouped.star")

        mdOptics = Table(fileName=fnData, tableName='optics')
        mdParts = Table(fileName=fnData, tableName='particles')
        mdGroups = Table(fileName=fnModel, tableName='model_groups')


        mdParts.addColumns('rlnGroupName=groupX')
        self.groupDict = dict()  # {rlnImageId:new_group_name}

        # Find out which optics group each scale group belongs to
        # Also initialise rlnGroupNrParticles for this selection
        # groupDict = dict()  # {groupNumber:opticsGroup}
        #
        # for row in mdParts:
        #     group_id = row.rlnGroupNumber
        #     part_optics_id = row.rlnOpticsGroup
        #
        #     if group_id not in groupDict:
        #         groupDict[group_id] = part_optics_id
        #     elif groupDict[group_id] != part_optics_id:
        #         self.warning("WARNING: group_no %d contains particles from multiple optics groups." % group_id)

        # First sort the mdGroups based on refined intensity scale factor
        mdGroups.sort('rlnGroupScaleCorrection')

        # Average group size
        nr_parts = mdParts.size()
        average_group_size = nr_parts // self.nrGroups.get()
        if average_group_size < 10:
            self.error("Each group should have at least 10 particles!")

        old_nr_groups = mdGroups.size()
        nr_parts_in_new_group = 0
        curr_group_id, my_old_group_id, new_group_id = 1, 1, 1
        for ig in range(0, old_nr_groups):
            # Now search for curr_group_id
            groupRow = mdGroups[ig]
            curr_group_id = groupRow.rlnGroupNumber
            if nr_parts_in_new_group > average_group_size:
                # This group is now full: start a new one
                new_group_id += 1
                nr_parts_in_new_group = 0

            new_group_name = "group_" + str(new_group_id)

            imgId = 0
            for row in mdParts:
                my_old_group_id = row.rlnGroupNumber
                if my_old_group_id == curr_group_id:
                    nr_parts_in_new_group += 1
                    #row.rlnGroupNumber = new_group_id
                    row = row._replace(rlnGroupName=new_group_name)
                    #self.groupDict[imgId] = new_group_name
                imgId += 1

        # new_group_names = dict()  # {groupNumber:groupName}
        # # Loop through all existing, sorted groups
        # new_group_id = 1
        # counter = 0
        #
        # for row in mdGroups:
        #     group_id = row.rlnGroupNumber
        #     nr_parts = groupNrPt
        #     nr_parts_in_new_group += nr_parts
        #
        #     if nr_parts_in_new_group > average_group_size:
        #         # This group is now full: start a new one
        #         new_group_id += 1
        #         nr_parts_in_new_group = 0
        #
        #     new_group_names[group_id] = "group_" + str(new_group_id)
        #
        # mdParts.addColumns('rlnGroupName=groupX')
        # for row in mdParts:
        #     group_id = row.rlnGroupNumber
        #     row.rlnGroupName = new_group_names[group_id]

        mdOut.removeColumns('rlnGroupNumber')  # no longer valid
        with open(fnOut, 'w') as f:
            mdOut.writeStar(f, tableName='particles')
            mdOptics.writeStar(f, tableName='optics')

        self.info("Regrouped particles into %d groups" % new_group_id)
        self.newGroupNr = new_group_id


    def createOutputStep(self):
        inputProt = self.inputProt.get()
        alignment = inputProt.outputParticles.getAlignment()
        partSet = self._createSetOfParticles()
        partSet.copyInfo(inputProt.outputParticles)
        outImagesMd = self._getExtraPath('particles_regrouped.star')

        convert.readSetOfParticles(
            outImagesMd, partSet,
            alignType=alignment,
            postprocessImageRow=self._postprocessImageRow)

        self._defineOutputs(outputParticles=partSet)
        self._defineSourceRelation(inputProt, partSet)

    # -------------------------- INFO functions -------------------------------
    def _summary(self):
        summary = []
        if not hasattr(self, 'outputParticles'):
            summary.append("Output particles not ready yet.")
        else:
            summary.append("Regrouped particles into %d groups" %
                           self.newGroupNr)
        return summary
    
    def _validate(self):
        errors = []

        if not (2 <= self.nrGroups.get() <= 999):
            errors.append("Number of groups must be between 2 and 999.")

        return errors

    # -------------------------- Utils functions ------------------------------
    def _postprocessImageRow(self, item, row):
        #print(row)
        id = getattr(row, 'rlnImageId')
        new_group_name = self.groupDict[id]
        item._rlnGroupName = String(new_group_name)

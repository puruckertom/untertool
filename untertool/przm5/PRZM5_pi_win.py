#!/usr/bin/python
#
def PRZM5_pi(pfac, snowmelt, evapDepth,
             uslek, uslels, uslep, fieldSize, ireg, slope, hydlength,
             canopyHoldup, rootDepth, canopyCover, canopyHeight,
             NumberOfFactors, useYears,
             USLE_day, USLE_mon, USLE_year, USLE_c, USLE_n, USLE_cn,
             firstyear, lastyear,
             dayEmerge_text, monthEmerge_text, dayMature_text, monthMature_text, dayHarvest_text, monthHarvest_text,
             addYearM, addYearH,
             irflag, tempflag,
             fleach, depletion, rateIrrig,
             albedo, bcTemp, Q10Box, soilTempBox1,
             numHoriz,
             SoilProperty_thick, SoilProperty_compartment, SoilProperty_bulkden, SoilProperty_maxcap,
             SoilProperty_mincap, SoilProperty_oc, SoilProperty_sand, SoilProperty_clay,
             rDepthBox, rDeclineBox, rBypassBox,
             eDepthBox, eDeclineBox,
             appNumber_year, totalApp,
             SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type, DepthIncorp, PestAppyRate,
             localEff, localSpray,
             PestDispHarvest,
             nchem, convert_Foliar1, parentTo3, deg1To2, foliarHalfLifeBox,
             koc_check, Koc,
             soilHalfLifeBox,
             convertSoil1, convert1to3, convert2to3):
    import os
    import stat
    import shutil
    import subprocess
    import zipfile
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
    import string
    import random
    import sys
    import przm5_input_generator

    print os.getcwd()
    import keys_Picloud_S3

    # Generate a random ID for file save
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    name_temp = id_generator()
    print name_temp

    ##########################################################################################
    #####AMAZON KEY, store output files. You might have to write your own import approach#####
    ##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey
    ##################################################################################
    ######Create a folder if it does not existed, where holds calculations' output.#####
    ##################################################################################
    cwd = os.path.dirname(os.path.realpath(__file__))
    print("cwd=" + cwd)

    src = cwd
    src1 = cwd + name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    ##
    os.chdir(src1)

    ################################################################################
    #####Write the PRZM5 input file################
    przm5_input_generator.test_przm5(pfac, snowmelt, evapDepth,
                                     uslek, uslels, uslep, fieldSize, ireg, slope, hydlength,
                                     canopyHoldup, rootDepth, canopyCover, canopyHeight,
                                     NumberOfFactors, useYears,
                                     USLE_day, USLE_mon, USLE_year, USLE_c, USLE_n, USLE_cn,
                                     firstyear, lastyear,
                                     dayEmerge_text, monthEmerge_text, dayMature_text, monthMature_text,
                                     dayHarvest_text, monthHarvest_text, addYearM, addYearH,
                                     irflag, tempflag,
                                     fleach, depletion, rateIrrig,
                                     albedo, bcTemp, Q10Box, soilTempBox1,
                                     numHoriz,
                                     SoilProperty_thick, SoilProperty_compartment, SoilProperty_bulkden,
                                     SoilProperty_maxcap, SoilProperty_mincap, SoilProperty_oc, SoilProperty_sand,
                                     SoilProperty_clay,
                                     rDepthBox, rDeclineBox, rBypassBox,
                                     eDepthBox, eDeclineBox,
                                     appNumber_year, totalApp,
                                     SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type,
                                     DepthIncorp, PestAppyRate, localEff, localSpray,
                                     PestDispHarvest,
                                     nchem, convert_Foliar1, parentTo3, deg1To2, foliarHalfLifeBox,
                                     koc_check, Koc,
                                     soilHalfLifeBox,
                                     convertSoil1, convert1to3, convert2to3)

    # ########Copy files to the tempt folder#############
    inp = "PRZM5.inp"
    met = "test.dvf"
    # print(os.listdir(src1))   #check what files are copied

    shutil.copy(os.path.join(src, "przm5_win.exe"), src1)
    shutil.copy(os.path.join(src, met), src1)
    print(os.getcwd())
    print(os.listdir(src1))  # check what files are copied

    src2 = os.path.join(src1, "przm5_win.exe")

    ##call the PRZM file
    os.chdir(src1)
    fname_before = os.listdir(src1)
    print 'Before running PRZM5', fname_before

    a = subprocess.Popen(src2, shell=0)
    print('done')
    a.wait()

    fname = os.listdir(src1)
    print 'After running PRZM5', fname

    Year = []
    Mon = []
    Day = []
    IRRG = []
    PRCP = []
    RUNF = []
    CEVP = []
    TETD = []
    IRRG_sum = []
    PRCP_sum = []
    PRCP_IRRG_sum = []
    RUNF_sum = []
    CEVP_sum = []
    TETD_sum = []
    CEVP_TETD_sum = []

    with open('test.zts') as f:
        next(f)
        next(f)
        next(f)
        for line in f:
            line = line.split()
            Year.append(int(line[0]))
            Mon.append(int(line[1]))
            Day.append(int(line[2]))
            IRRG.append(float(line[3]))
            PRCP.append(float(line[4]))
            RUNF.append(float(line[5]))
            CEVP.append(float(line[6]))
            TETD.append(float(line[7]))

    year_ind = [Year.index(i) for i in list(set(Year))]
    year_ind.append(len(Year))

    for jj in range(len(year_ind) - 1):
        PRCP_sum.append(sum(PRCP[year_ind[jj]:year_ind[jj + 1]]))
        IRRG_sum.append(sum(IRRG[year_ind[jj]:year_ind[jj + 1]]))
        PRCP_IRRG_sum = [x + y for (x, y) in zip(PRCP_sum, IRRG_sum)]
        RUNF_sum.append(sum(RUNF[year_ind[jj]:year_ind[jj + 1]]))
        CEVP_sum.append(sum(CEVP[year_ind[jj]:year_ind[jj + 1]]))
        TETD_sum.append(sum(TETD[year_ind[jj]:year_ind[jj + 1]]))
        CEVP_TETD_sum = [x + y for (x, y) in zip(CEVP_sum, TETD_sum)]

    ##zip all the file
    zout = zipfile.ZipFile("test.zip", "w", zipfile.ZIP_DEFLATED)
    for name in fname:
        if name != 'przm5_win.exe' and name != 'test.dvf':
            zout.write(name)
    zout.close()

    ##upload file to S3
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'przm5')
    k = Key(bucket)

    name1 = 'PRZM5_' + name_temp + '.zip'
    k.key = name1
    link = 'https://s3.amazonaws.com/przm5/' + name1
    print link

    # return link, PRCP_IRRG_sum, RUNF_sum, CEVP_TETD_sum, src1, name1

    k.set_contents_from_filename('test.zip')

    k.set_acl('public-read-write')
    print 'upload finished'
    os.chdir(src)
    shutil.rmtree(src1)

    return link, PRCP_IRRG_sum, RUNF_sum, CEVP_TETD_sum, src1, name1

    # return 'done'

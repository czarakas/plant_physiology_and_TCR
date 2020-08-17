import numpy as np
sperday=86400
def grab_cmip_dataset(cdict, Mname,Rname,Vname):
    
    nametag =Mname +'_' +Rname +'_' +Vname
    #print('getting dataset for: ' +nametag)
    
    if nametag in cdict:
        DS = cdict[nametag] # open the dataset
        
    elif Vname== 'RUNOFF': # convert units
        unitconversion=sperday
        oldname='mrro'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
        
    elif Vname == 'PRECIP': # convert units
        unitconversion=sperday
        oldname='pr'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
        
    elif Vname == 'GPP': # convert units
        unitconversion=sperday
        oldname='gpp'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
        
    elif Vname == 'ET': # convert units
        unitconversion=sperday
        oldname='evspsbl'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
    
    elif Vname == 'ET_veg': # convert units
        unitconversion=sperday
        oldname='evspsblveg'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
    
    elif Vname == 'TRAN': # convert units
        unitconversion=sperday
        oldname='tran'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        if oldnametag in cdict:
            DS = cdict[oldnametag] # open the dataset
            oldarray = DS[oldname] # get the values
            DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
        
    elif Vname == 'EVAP': # convert units
        unitconversion=sperday
        oldname1='tran'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldname2='evspsbl'
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        
        if ((oldnametag1 in cdict) and (oldnametag2 in cdict)):
            DS = cdict[oldnametag1] # open the dataset
            tran = DS[oldname1] # get the values
            DS2 = cdict[oldnametag2] # open the dataset
            DS2 = DS2.reindex_like(DS, method='nearest')
            et = DS2[oldname2] # get the values
            DS[Vname]=(et-tran)*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' not in the dictionary')
            return #exit here
    
    elif Vname == 'TRANperLAI': # convert units
        unitconversion=sperday
        oldname='tran'
        oldnametag = Mname +'_' +Rname +'_' +oldname
        oldname2='lai'
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if ((oldnametag in cdict) and (oldnametag2 in cdict)):
            DS = cdict[oldnametag] # open the dataset
            transpiration = DS[oldname] # get the values
            DS2 = cdict[oldnametag2] # open the dataset
            DS2 = DS2.reindex_like(DS, method='nearest')
            
            
            leafArea = DS2[oldname2] # get the values
            
            DS[Vname]=(transpiration/leafArea)*unitconversion # convert the unit in the dataset
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag +' not in the dictionary')
            return #exit here
    
    elif nametag == 'CanESM2_1pctCO2_hurs': #correct the units due to error in the original dataset
        unitconversion=100
        DS = cdict[nametag] # open the dataset
        oldarray = DS[Vname] # get the values
        DS[Vname]=oldarray*unitconversion # convert the unit in the dataset

    elif nametag == 'IPSL-CM5A-LR_1pctCO2_mrro': #correct the units due to error in the original dataset
        unitconversion=48
        DS = cdict[nametag] # open the dataset
        oldarray = DS[Vname] # get the values
        DS[Vname]=oldarray*unitconversion # convert the unit in the dataset
    
    elif Vname == 'WUE': # create a variable from multiple variables
        # WUE=gC/water lost
        # gpp is in kgC/m2/s => convert to gC/m2/s
        # tran is in kgwater/m2/s
        # WUE = gpp/tran = gC/kgwater
        unitconversion=1e-3
        oldnametag1 = Mname +'_' +Rname +'_' +'gpp'
        oldnametag2 = Mname +'_' +Rname +'_' +'tran'
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            oldarray1 = DS['gpp'] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            oldarray2 = DS2['tran'] # get the values
            wuetmp=(oldarray1/oldarray2)*unitconversion #np.multiply(np.divide(oldarray1,oldarray2),unitconversion) # convert the unit in the dataset
            DS[Vname]= np.minimum(wuetmp,100)
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')
            return #exit here
        
    elif Vname == 'albedo': # create a variable from multiple variables
        oldnametag1 = Mname +'_' +Rname +'_' +'rsds'
        oldnametag2 = Mname +'_' +Rname +'_' +'rsus'
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            oldarray1 = DS['rsds'] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            oldarray2 = DS2['rsus'] # get the values
            albedo=(oldarray2/oldarray1)
            DS[Vname]=albedo
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')
            return #exit here

    elif Vname == 'VPD': # create a variable from multiple variables
        unitconversion=1e-3
        Rv=461 # J/kg/K
        oldnametag1 = Mname +'_' +Rname +'_' +'hurs'
        oldnametag2 = Mname +'_' +Rname +'_' +'tas'
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RH = DS['hurs'] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            T = DS2['tas'] # get the values
            T = T - 273.15 #convert from K to C
            RH = RH/100 #convert from scale of percent to fraction
            estarT = 610.8*np.exp(Lv/Rv*(1/273.15 - 1/(T + 273.15)))  #T in celsius, final unit Pa
            VPD=estarT*(1-RH)    
            DS[Vname]=VPD # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here
    
    elif Vname == 'Forcing_TOA': # create a variable from multiple variables
        oldnametag1 = Mname +'_' +Rname +'_' +'rsut'
        oldnametag2 = Mname +'_' +Rname +'_' +'rsdt'
        oldnametag3 = Mname +'_' +Rname +'_' +'rlut'
        if (oldnametag1 in cdict and oldnametag2 in cdict and oldnametag3 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RSUT = DS['rsut'] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            RSDT = DS2['rsdt'] # get the values
            DS3= cdict[oldnametag3] # open the dataset
            RLUT = DS3['rlut'] # get the values
            
            TOA_net = RSDT - RSUT - RLUT
            
            DS[Vname]=TOA_net # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' or ' +oldnametag3 +' not in the dictionary')    
            return #exit here
        
    elif Vname == 'PmE': # create a variable from multiple variables
        unitconversion=1e-3
        oldname1='pr'
        oldname2='evspsbl'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            P = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            E = DS2[oldname2]*sperday # get the values
 
            DS[Vname]=P-E # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here    
    
    elif Vname == 'rsds_clouds': # create a variable from multiple variables
        oldname1='rsds'
        oldname2='rsdscs'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RSDS = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            RSDSCS = DS2[oldname2] # get the values
 
            DS[Vname] = RSDS - RSDSCS      
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here   
        
    elif Vname == 'rlds_clouds': # create a variable from multiple variables
        oldname1='rlds'
        oldname2='rldscs'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RLDS = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            RLDSCS = DS2[oldname2] # get the values
 
            DS[Vname] = RLDS - RLDSCS      
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
        
    elif Vname == 'rad_clouds': # create a variable from multiple variables
        oldname1='rlds'
        oldname2='rldscs'
        oldname3='rsds'
        oldname4='rsdscs'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        oldnametag3 = Mname +'_' +Rname +'_' +oldname3
        oldnametag4 = Mname +'_' +Rname +'_' +oldname4
        
        if (oldnametag1 in cdict and oldnametag2 in cdict and oldnametag3 in cdict and oldnametag4 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RLDS = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            RLDSCS = DS2[oldname2] # get the values
            DS3 = cdict[oldnametag3] # open the dataset
            RSDS = DS3[oldname3] # get the values
            DS4= cdict[oldnametag4] # open the dataset
            RSDSCS = DS4[oldname4] # get the values
 
            RLDS_CLOUDS = RLDS - RLDSCS      
            RSDS_CLOUDS = RSDS - RSDSCS  
            DS[Vname] = RLDS_CLOUDS+RSDS_CLOUDS
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
    
    elif Vname == 'SWnet': # create a variable from multiple variables
        oldname1='rsus'
        oldname2='rsds'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            SW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            SW_down = DS2[oldname2] # get the values
 
            DS[Vname] = SW_down - SW_up # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
    
    elif Vname == 'SWnet': # create a variable from multiple variables
        oldname1='rsus'
        oldname2='rsds'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            SW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            SW_down = DS2[oldname2] # get the values
 
            DS[Vname] = SW_down - SW_up # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
    
    elif Vname == 'LWnet': # create a variable from multiple variables
        oldname1='rlus'
        oldname2='rlds'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            LW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LW_down = DS2[oldname2] # get the values
 
            DS[Vname] = LW_down - LW_up # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
    
    elif Vname == 'LWnet_CS': # create a variable from multiple variables
        oldname1='rluscs'
        oldname2='rldscs'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            LW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LW_down = DS2[oldname2] # get the values
 
            DS[Vname] = LW_down - LW_up # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
    
    elif Vname == 'LWnet_clouds': # create a variable from multiple variables
        oldname1='rluscs'
        oldname2='rldscs'
        oldname3='rlus'
        oldname4='rlds'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        oldnametag3 = Mname +'_' +Rname +'_' +oldname3
        oldnametag4 = Mname +'_' +Rname +'_' +oldname4
        if ((oldnametag1 in cdict) and (oldnametag2 in cdict) and (oldnametag3 in cdict) and (oldnametag4 in cdict)):
            DS = cdict[oldnametag1] # open the dataset
            LW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LW_down = DS2[oldname2] # get the values
            LWnet_CS = LW_down - LW_up
            
            DS = cdict[oldnametag3] # open the dataset
            LW_up = DS[oldname3] # get the values
            DS2= cdict[oldnametag4] # open the dataset
            LW_down = DS2[oldname4] # get the values
            LWnet_full = LW_down - LW_up
 
            DS[Vname] = LWnet_full - LWnet_CS     
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' or '+oldnametag3 +' or ' +oldnametag4+' not in the dictionary')    
            return #exit here
    
    elif Vname == 'SH+LH': # create a variable from multiple variables
        oldname1='hfss'
        oldname2='hfls'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            SH = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LH = DS2[oldname2] # get the values
 
            DS[Vname] = SH+LH # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
    
    elif Vname == 'BowenRatio': # create a variable from multiple variables
        oldname1='hfss'
        oldname2='hfls'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            SH = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LH = DS2[oldname2] # get the values
 
            DS[Vname] = SH/LH # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
        
    elif Vname == 'EF': # create a variable from multiple variables
        oldname1='hfss'
        oldname2='hfls'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            SH = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LH = DS2[oldname2] # get the values
 
            DS[Vname] = LH/(SH+LH) # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
        
    elif Vname == 'Tgrad': # create a variable from multiple variables
        oldname1='ts'
        oldname2='tas'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            ts = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            tas = DS2[oldname2] # get the values
 
            DS[Vname] = ts - tas # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here 
    
    elif Vname == 'Rnet_surf': # create a variable from multiple variables
        oldname1='rlus'
        oldname2='rlds'
        oldname3='rsus'
        oldname4='rsds'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        oldnametag3 = Mname +'_' +Rname +'_' +oldname3
        oldnametag4 = Mname +'_' +Rname +'_' +oldname4
        if ((oldnametag1 in cdict) and (oldnametag2 in cdict) and (oldnametag3 in cdict) and (oldnametag4 in cdict)):
            DS = cdict[oldnametag1] # open the dataset
            LW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LW_down = DS2[oldname2] # get the values
            DS3 = cdict[oldnametag3] # open the dataset
            SW_up = DS3[oldname3] # get the values
            DS4= cdict[oldnametag4] # open the dataset
            SW_down = DS4[oldname4] # get the values
 
            DS[Vname] = LW_down - LW_up + SW_down - SW_up # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
    
    elif Vname == 'G': # create a variable from multiple variables
        oldname1='rlus'
        oldname2='rlds'
        oldname3='rsus'
        oldname4='rsds'
        oldname5='hfls'
        oldname6='hfss'
        oldnametag1 = Mname +'_' +Rname +'_' +oldname1
        oldnametag2 = Mname +'_' +Rname +'_' +oldname2
        oldnametag3 = Mname +'_' +Rname +'_' +oldname3
        oldnametag4 = Mname +'_' +Rname +'_' +oldname4
        oldnametag5 = Mname +'_' +Rname +'_' +oldname5
        oldnametag6 = Mname +'_' +Rname +'_' +oldname6
        if ((oldnametag1 in cdict) and (oldnametag2 in cdict) and (oldnametag3 in cdict) and (oldnametag4 in cdict) and (oldnametag5 in cdict) and (oldnametag6 in cdict)):
            DS = cdict[oldnametag1] # open the dataset
            LW_up = DS[oldname1] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            LW_down = DS2[oldname2] # get the values
            DS3 = cdict[oldnametag3] # open the dataset
            SW_up = DS3[oldname3] # get the values
            DS4= cdict[oldnametag4] # open the dataset
            SW_down = DS4[oldname4] # get the values
            DS5= cdict[oldnametag5] # open the dataset
            LH = DS5[oldname5] # get the values
            DS6= cdict[oldnametag6] # open the dataset
            SH = DS6[oldname6] # get the values
 
            DS[Vname] = LW_down - LW_up + SW_down - SW_up - LH - SH # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' not in the dictionary')    
            return #exit here  
        
    elif Vname == 'Q': # create a variable from multiple variables
        # Q is specific humidity at the surface in units of kg water/kg air
        # hurs is in %
        # tas is in kelvin
        # ps is surface pressure in Pa
        unitconversion=1e-3
        Rv=461 # J/kg/K
        oldnametag1 = Mname +'_' +Rname +'_' +'hurs'
        oldnametag2 = Mname +'_' +Rname +'_' +'tas'
        oldnametag3 = Mname +'_' +Rname +'_' +'ps'
        if (oldnametag1 in cdict and oldnametag2 in cdict):
            DS = cdict[oldnametag1] # open the dataset
            RH = DS['hurs'] # get the values
            DS2= cdict[oldnametag2] # open the dataset
            T = DS2['tas'] # get the values
            T = T - 273.15 #convert from K to C
            DS3= cdict[oldnametag3] # open the dataset
            PS = DS3['ps'] # get the values
            RH = RH/100 #convert from scale of percent to fraction
            estarT = 610.8*np.exp(Lv/Rv*(1/273.15 - 1/(T + 273.15)))  #T in celsius, final unit Pa
            Q=0.622*RH*estarT/PS   # final unit in kg/kg
            DS[Vname]=Q # convert the unit in the dataset        
        else: # it isn't a variable/model/run combo in the dictionary
            print(oldnametag1 +' or ' +oldnametag2 +' or ' +oldnametag3 +' not in the dictionary')    
            return #exit here   
        
    else: # it isn't a variable/model/run combo in the dictionary
        print(nametag +' not in the dictionary')
        return #exit here
    
    return DS
from django.shortcuts import render
import pandas as pd
import numpy as np
import json

# Create your views here.

#HEERF


def heerf(request):
    heerf_csv=pd.read_csv('https://raw.githubusercontent.com/oilfieldrando/HEERF_final/main/heerf_final2.csv')
    states=['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Marshall Islands', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Virgin Islands', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia','Wyoming','Wisconsin','Palau']
    state_name=request.POST.get('inputState')
    
    

    if request.POST.get('chart_view'):
        chart_view = request.POST.get('chart_view')
        if request.POST.get('chart_view')=='Totals by State':
            view_type='chart1'
            

        elif request.POST.get('chart_view')=='50 Biggest Payouts':
            view_type='chart2'

        elif request.POST.get('chart_view')=='50 Richest Colleges':
            view_type='chart3'
    else:
        chart_view = 'Totals by State'
        view_type = 'chart1'
    
    if request.POST.get('view_type1'):
        chart_view = 'Totals by State'
        view_type = request.POST.get('view_type1')

    elif request.POST.get('view_type2'):
        chart_view = '50 Biggest Payouts'
        view_type = request.POST.get('view_type2')

    elif request.POST.get('view_type3'):
        chart_view = '50 Richest Colleges'
        view_type = request.POST.get('view_type3')

    else: 
        if chart_view == 'Totals by State':
            view_type = 'chart1'
        elif chart_view == '50 Biggest Payouts':
            view_type = 'chart2'
        else:
            view_type = 'chart3'

    
    inst_name=request.POST.get('inputInst')  
    heerf_csv.sort_values(by=['institution'], inplace=True, ascending=True)
    inst_list=heerf_csv[heerf_csv['state_full']==state_name][heerf_csv.columns[1]].tolist()
    inst_count=len(inst_list)

    
    # Relief by State
    
    state_totals = pd.DataFrame({'state':[],'cares_act':[],'omnibus':[],'amer_rescue_act':[],'total_relief':[]})
    for x in states:
        state_data=heerf_csv[heerf_csv['state_full']==x]
        state_totals=state_totals.append({'state':x,'cares_act':state_data.iloc[:,[3]].sum(),'omnibus':state_data.iloc[:,[4]].sum(),'amer_rescue_act':state_data.iloc[:,[5]].sum(),'total_relief':state_data.iloc[:,[6]].sum()}, ignore_index=True)
        state_totals=state_totals.astype({"total_relief":'float',"cares_act":'float',"omnibus":'float',"amer_rescue_act":'float'})
        state_totals=state_totals.sort_values(by='total_relief',ascending=False)    
        state_labels = list(state_totals['state'].values)
        state_cares = list(state_totals['cares_act'].values)
        state_omnibus = list(state_totals['omnibus'].values)
        state_ara = list(state_totals['amer_rescue_act'].values)
        total_relief = list(state_totals['total_relief'].values)
        
        
    allData=[]
    for i in range(state_totals.shape[0]):
        temp=state_totals.loc[i]
        allData.append(dict(temp))


    # Top Recipients
    heerf_csv.sort_values(by=['total_relief'],inplace=True,ascending=False)
    top50 = heerf_csv.iloc[:50]
    t50_labels = top50['institution'].values.tolist()
    t50_cares = top50['cares_act'].values.tolist()
    t50_omnibus = top50['omnibus'].values.tolist()
    t50_ara = top50['amer_rescue_act'].values.tolist()
    t50_total = top50['total_relief'].values.tolist()

    top50_data = []
    for i in range(top50.shape[0]):
        temp=top50.loc[i]
        top50_data.append(dict(temp))

    # Rich Recipients
    
    heerf_csv.sort_values(by=['endowment'],inplace=True,ascending=False)
    rich50 = heerf_csv.iloc[:50].reset_index()
    rich50_labels = rich50['institution'].values.tolist()
    rich50_cares = rich50['cares_act'].values.tolist()
    rich50_omnibus = rich50['omnibus'].values.tolist()
    rich50_ara = rich50['amer_rescue_act'].values.tolist()
    rich50_total = rich50['total_relief'].values.tolist()

    rich50_data = []
    for i in range(rich50.shape[0]):
        temp2=rich50.loc[i]
        rich50_data.append(dict(temp2))
    
     
    context={
        'inst_list':inst_list,
        'state_name':state_name,
        'data':allData,
        'states':states, 
        'state_labels':state_labels,
        'total_relief':total_relief, 
        'state_cares':state_cares, 
        'state_omnibus':state_omnibus,
        'state_ara':state_ara,
        't50_labels':t50_labels,
        't50_cares':t50_cares,
        't50_omnibus':t50_omnibus,
        't50_ara':t50_ara,
        't50_total':t50_total,
        'top50_data':top50_data,
        'rich50_data':rich50_data,
        'rich50_labels':rich50_labels,
        'rich50_cares':rich50_cares,
        'rich50_omnibus':rich50_omnibus,
        'rich50_ara':rich50_ara,
        'rich50_total':rich50_total,
        'chart_view':chart_view,
        'view_type':view_type,
        
        }
    return render(request,'heerf.html',context)

def heerf_state(request):
    # Lookup Bars
    states=['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Marshall Islands', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Virgin Islands', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia','Wyoming','Wisconsin','Palau']
    
    if request.POST.get('inputState'):
        state_name=request.POST.get('inputState')
    else:
        state_name='Alabama'
    inst_name=request.POST.get('inputInst')
    heerf_csv=pd.read_csv('https://raw.githubusercontent.com/oilfieldrando/HEERF_final/main/heerf_final2.csv')  
    heerf_csv.sort_values(by=['institution'], inplace=True, ascending=True)
    inst_list=heerf_csv[heerf_csv['state_full']==state_name][heerf_csv.columns[1]].tolist()
    inst_count=len(inst_list)
    
    

    # State totals graph
    state_totals = pd.DataFrame({'state':[],'cares_act':[],'omnibus':[],'amer_rescue_act':[],'total_relief':[]})
    for x in states:
        state_data=heerf_csv[heerf_csv['state_full']==state_name]
        state_totals=state_totals.append({'state':x,'cares_act':state_data.iloc[:,[3]].sum(),'omnibus':state_data.iloc[:,[4]].sum(),'amer_rescue_act':state_data.iloc[:,[5]].sum(),'total_relief':state_data.iloc[:,[6]].sum()}, ignore_index=True)
        state_totals=state_totals.astype({"total_relief":'float',"cares_act":'float',"omnibus":'float',"amer_rescue_act":'float'})
        state_totals=state_totals.sort_values(by='total_relief',ascending=False) 
    state_detail = pd.DataFrame(state_totals[state_totals['state']==state_name][state_totals.columns[0:]])
    
    cares=state_detail.iloc[0,1]
    omnibus=state_detail.iloc[0,2]
    ara=state_detail.iloc[0,3]
    state_total=state_detail.iloc[0,4]


    # Institution Table
    
    heerf_csv.sort_values(by=['total_relief'], inplace=True, ascending=False)
    inst_data = heerf_csv[heerf_csv['state_full']==state_name].iloc[0:].reset_index()
    inst_data = inst_data.astype({"total_relief":'float'})
    
    inst_set = []
    for i in range(inst_data.shape[0]):
        temp1=inst_data.loc[i]
        inst_set.append(dict(temp1))

    inst_code_set = []
    heerf_csv.sort_values(by=['institution'], inplace=True, ascending=True)
    inst_data2 = heerf_csv[heerf_csv['state_full']==state_name].iloc[0:].reset_index()
    
    for i in range(inst_data2.shape[0]):
        temp2=inst_data2.loc[i]
        inst_code_set.append(dict(temp2))

    # Inst graph
    inst_df=pd.DataFrame(heerf_csv[heerf_csv['state_full']==state_name])
    inst_df.columns=['inst_st','inst','inst_state','inst_cares','inst_omnibus','inst_ara','inst_total','endowment','code']
    inst_labels=inst_df['inst'].values.tolist()
    inst_totals=inst_df['inst_total'].values.tolist()
    
    context={
        'states':states,
        'state_name':state_name,
        'inst_list':inst_list,
        'inst_name':inst_name,
        'state_detail':state_detail,
        'cares':cares,
        'omnibus':omnibus,
        'ara':ara,
        'state_total':state_total,
        'inst_set':inst_set,
        'inst_labels':inst_labels,
        'inst_totals':inst_totals,
        'inst_count':inst_count,
        'inst_code_set':inst_code_set 
    }
    return render(request, 'heerf_main.html', context)

def heerf_inst(request):
    heerf_csv=pd.read_csv('https://raw.githubusercontent.com/oilfieldrando/HEERF_final/main/heerf_final2.csv')

    # Inputs
    states=['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Marshall Islands', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Virgin Islands', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia','Wyoming','Wisconsin','Palau']
    
    if request.POST.get('inputState'):
        state_name=request.POST.get('inputState')
    else:
        state_name='Massachusettes'
    
    
    
    if request.POST.get('inputInst'):
        inst_name=int(request.POST.get('inputInst'))
    
    else:
        inst_name= 215500


    # Institution totals graph   
    inst_data = pd.DataFrame(heerf_csv[heerf_csv['inst_id']==inst_name][heerf_csv.columns[0:]])
    heerf_csv.sort_values(by=['institution'], inplace=True, ascending=True)
    inst = inst_data.iloc[0,1]
    state_name = inst_data.iloc[0,2]
    cares=inst_data.iloc[0,3]
    omnibus=inst_data.iloc[0,4]
    ara=inst_data.iloc[0,5]
    inst_total=inst_data.iloc[0,6]
    endowment=inst_data.iloc[0,7]

    inst_code_set = []
    heerf_csv.sort_values(by=['institution'], inplace=True, ascending=True)
    inst_data2 = heerf_csv[heerf_csv['state_full']==state_name].iloc[0:].reset_index()
    
    for i in range(inst_data2.shape[0]):
        temp2=inst_data2.loc[i]
        inst_code_set.append(dict(temp2))
    
    
    context={
    'states':states,
    'state_name':state_name,
    'inst_name':inst_name,
    'cares':cares,
    'omnibus':omnibus,
    'ara':ara,
    'inst_total':inst_total,
    'endowment':endowment,
    'inst':inst,
    'inst_code_set':inst_code_set
    }
    return render(request, 'heerf_lookup.html', context)



# SVOG

def svog(request):
    # Initialize
    url='https://raw.githubusercontent.com/oilfieldrando/svog/main/svogdata_v11.csv'
    svog = pd.read_csv(url)
    if request.POST.get('data_view'):
        data_view = request.POST.get('data_view')
        if request.POST.get('data_view')=='Totals by State':
            view_type = 'states_chart'
        elif request.POST.get('data_view')=='$10 Million Club':
            view_type = 'max_table'
            
    else:
        data_view = 'Totals by State'
        view_type = 'states_chart'


    if request.POST.get('view_type1'):
        data_view = 'Totals by State'
        view_type = request.POST.get('view_type1')


    #Lookup
    state_list = svog[svog.columns[6]].tolist()
    state_list = list(dict.fromkeys(state_list))
    state = request.POST.get('inputState')
    city = request.POST.get('inputCity')
    
    

    if data_view == 'Totals by State':
        # State totals chart
        state_svog = pd.DataFrame({'state':[],'total':[]})
        for x in state_list:
            state_svog_data=svog[svog['state_full']==x]
            state_svog=state_svog.append({'state':x,'total':state_svog_data.iloc[:,[0]].sum()}, ignore_index=True)
            state_svog=state_svog.astype({"total":'float'})
            state_svog=state_svog.sort_values(by='total',ascending=False)    
            state_svog_labels = list(state_svog['state'].values)
            state_svog_totals = list(state_svog['total'].values)
    
         # State totals table
        svogData=[]
        for i in range(state_svog.shape[0]):
            temp=state_svog.loc[i]
            svogData.append(dict(temp))
        
        context={
        'state_list':state_list,
        'state':state,
        'state_svog_labels':state_svog_labels,
        'state_svog_totals':state_svog_totals,
        'svogData':svogData,
        'data_view':data_view,
        'view_type':view_type,
        
        }

    else:
        # Max grantees
        max_grants = svog[svog['amount']==10000000].iloc[0:].reset_index()
        max_grants_set=[]
        for i in range(max_grants.shape[0]):
            temp2=max_grants.loc[i]
            max_grants_set.append(dict(temp2))

        context={
        'state_list':state_list,
        'state':state,       
        'data_view':data_view,
        'view_type':view_type,
        'max_grants_set':max_grants_set,
        }
    

    

    return render(request, 'svog/initial.html', context)

def svog_state(request):
    # Initialize
    url='https://raw.githubusercontent.com/oilfieldrando/svog/main/svogdata_v11.csv'
    svog = pd.read_csv(url)
    
    if request.POST.get('data_view'):
        data_view = request.POST.get('data_view')
    else:
        data_view = 'Top City Payouts'

    if request.POST.get('inputState'):
        state = request.POST.get('inputState')
    else:
        state = 'New York'

    # State/City select list
    state_list = svog[svog.columns[6]].tolist()
    state_list = list(dict.fromkeys(state_list))
    city = request.POST.get('inputCity')
    city_set_raw=pd.DataFrame(svog[svog['state_full']==state].iloc[:,3:5],columns=['city','city_id'])
    city_set=city_set_raw.drop_duplicates(subset=['city_id']).reset_index()
    city_list_order = city_set.reset_index().to_json(orient = 'records')
    city_list = []
    city_list = json.loads(city_list_order)
    venue_set = svog[svog['state_full']==state].reset_index()
    venue_list = venue_set.sort_values(by='venue', ascending=True)
    venue_list_tableset = venue_list.reset_index().to_json(orient = 'records')
    venues_list_data = []
    venue_list_data = json.loads(venue_list_tableset)

    # Variables
    state_total = svog[svog['state_full']==state].iloc[:,[0]].sum()
    total_grantees = total_grantees = len(svog[svog['state_full']==state][svog.columns[1]].tolist())
    percent_share = (state_total/(svog['amount'].sum()))*100

    if data_view == 'Top City Payouts':
        # Top Recipients by City table
        cities = list(city_set['city_id'].values)
        city_svog = pd.DataFrame({'city':[],'city_id':[],'total':[]})
        for x in cities:
            city_svog_data = svog[svog['city_id']==x]
            city_svog = city_svog.append({'city':city_svog_data.iloc[0,3],'city_id':x,'total':city_svog_data.iloc[:,[0]].sum()},ignore_index=True)
            city_svog = city_svog.astype({'total':'float','city_id':'int'})
            city_svog = city_svog.sort_values(by=['total'], ascending=False)
            city_svog =  city_svog.iloc[0:20,:]
    
        city_table = city_svog.reset_index().to_json(orient = 'records')
        data = []
        data = json.loads(city_table)

        context={
        'state_list':state_list,
        'city_list':city_list,
        'state':state,
        'city':city,
        'data':data,
        'data':data,
        'venue_list_data':venue_list_data,
        'data_view':data_view,
        'state_total':state_total,
        'total_grantees':total_grantees,
        'percent_share':percent_share,
        
    }
    else:
        # Top Recipients Venues in State
        top_25=svog[svog['state_full']==state].sort_values(by=['amount'], ascending=False).iloc[:25].reset_index()
        top_25_tableset = top_25.reset_index().to_json(orient = 'records')
        top_25_data = []
        top_25_data = json.loads(top_25_tableset)

        context={
        'state_list':state_list,
        'city_list':city_list,
        'state':state,
        'city':city,
        'top_25_data':top_25_data,
        'data_view':data_view,
        'venue_list_data':venue_list_data,
    }
    
    
  
    return render(request, 'svog/svog_state.html', context)

def svog_city(request):
    # initialize
    url='https://raw.githubusercontent.com/oilfieldrando/svog/main/svogdata_v11.csv'
    svog = pd.read_csv(url)

    if request.POST.get('inputCity'):
        city = request.POST.get('inputCity')
    else:
        city = str(2508)
    
    venue_set = svog[svog['city_id']==int(city)].reset_index()
    state = venue_set.iloc[0,7]
    city_name = venue_set.iloc[0,4]

    # Lookup
    state_list = svog[svog.columns[6]].tolist()
    state_list = list(dict.fromkeys(state_list))
    city_set_raw=pd.DataFrame(svog[svog['state_full']==state].iloc[:,3:5],columns=['city','city_id'])
    city_set=city_set_raw.drop_duplicates(subset=['city_id']).reset_index()
    city_list_order = city_set.reset_index().to_json(orient = 'records')
    city_list = []
    city_list = json.loads(city_list_order)
    venue_list = venue_set.sort_values(by='venue', ascending=True)
    venue_list_tableset = venue_list.reset_index().to_json(orient = 'records')
    venues_list_data = []
    venue_list_data = json.loads(venue_list_tableset)

    # Variables
    city_total = venue_set.iloc[:,[1]].sum()
    city_grantees  = venue_set.shape[0]

    # Top venues
    venues_desc = venue_set.sort_values(by='amount', ascending=False)
    venues_desc_tableset = venues_desc.reset_index().to_json(orient = 'records')
    venues_desc_data = []
    venues_desc_data = json.loads(venues_desc_tableset)


    context={
        'state_list':state_list,
        'state':state,
        'city_name':city_name,
        'venues_desc_data':venues_desc_data,
        'city_list':city_list,
        'venue_list_data':venue_list_data,
        'city_total':city_total,
        'city_grantees':city_grantees,
  
    }

    return render(request, 'svog/svog_city.html', context)

def svog_venue(request):
    # Initialize
    url='https://raw.githubusercontent.com/oilfieldrando/svog/main/svogdata_v11.csv'
    svog = pd.read_csv(url)

    if request.POST.get('inputVenue'):
        venue=(request.POST.get('inputVenue'))
    
    else:
        venue= 7928
    
    # Venue Data
    venue_data = svog[svog['inst_id']==int(venue)].reset_index()
    venue_detail=[]
    for i in range(venue_data.shape[0]):
            temp2=venue_data.loc[i]
            venue_detail.append(dict(temp2))
    

    
    # Lookup
    state  = venue_data.iloc[0,7]
    city_name = venue_data.iloc[0,4]
    city_id = venue_data.iloc[0,5]
    venue_name = venue_data.iloc[0,2]
    state_list = svog[svog.columns[6]].tolist()
    state_list = list(dict.fromkeys(state_list))
    city_set_raw=pd.DataFrame(svog[svog['state_full']==state].iloc[:,3:5],columns=['city','city_id'])
    city_set=city_set_raw.drop_duplicates(subset=['city_id']).reset_index()
    city_list_order = city_set.reset_index().to_json(orient = 'records')
    city_list = []
    city_list = json.loads(city_list_order)
    venue_set = svog[svog['city_id']==int(city_id)].reset_index()
    venue_list = venue_set.sort_values(by='venue', ascending=True)
    venue_list_tableset = venue_list.reset_index().to_json(orient = 'records')
    venue_list_data = []
    venue_list_data = json.loads(venue_list_tableset)

    context={
        'venue_detail':venue_detail,
        'state_list':state_list,
        'city_list':city_list,
        'venue_list_data':venue_list_data,
        'state':state,
        'city_name':city_name,
        'venue_name':venue_name,

    }
    return render(request, 'svog/svog_venue.html', context)








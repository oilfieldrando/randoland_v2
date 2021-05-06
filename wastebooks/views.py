from django.shortcuts import render
import pandas as pd
import numpy as np

# Create your views here.

#HEERF

heerf_csv=pd.read_csv('https://raw.githubusercontent.com/oilfieldrando/HEERF_final/main/heerf_final2.csv')
def heerf(request):
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
    heerf_csv=pd.read_csv('https://raw.githubusercontent.com/oilfieldrando/HEERF_final/main/heerf_final2.csv')  
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


# Coronavirus Relief Fund 1


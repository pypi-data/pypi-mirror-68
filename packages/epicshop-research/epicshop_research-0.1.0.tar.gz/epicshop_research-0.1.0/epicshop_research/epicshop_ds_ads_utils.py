class Utils:
  def Ads(shop):
    active_ads = adsFeed(shop, date_range=100, bd=True, filters='active')
    paused_ads = adsFeed(shop, date_range=7, bd=True, filters='paused')
    _ads_utils_daily_stop(adsets = active_ads)
    _ads_utils_daily_restart(adsets = paused_ads)
    try: shop.ff.quit()
    except: pass
  def Ads_Duplicate(shop):
    """
    Download All Ad Sets
    Get All Campaigns via API
    For each Campaign:
      Get All Ads
      Targeting_Spec_Dict keying Ads Targeting_Specs
      
      For Each Targeting_Spec:
        Create a current_budget_list
        Discover count new_budgets
        Duplicate the $5 ad set Accordingly to the count_new_budgets & current_budget_list
    """
    count_of_newly_created_adsets = 0
    sum_of_newly_created_adsets_budget = 0

    #Download All Ad Sets
    csv_adsets = None
    if datetime.now().hour in [0,1,2]:
      csv_adsets = adsFeed(shop, date_range=1, bd=True, filters=None)
    else:
      csv_adsets = adsFeed(shop, date_range=0, bd=True, filters=None)

    errors=0

    #Create a Group of Active Campaign IDs
    campaigns = shop.fb.get_campaigns(params={'limit':9000})
    for campaign in campaigns:
      major_dict = {}
      adsets = campaign.get_ad_sets()
      for adset in adsets:
        targeting_spec = '%s' % adset.remote_read(fields=['targeting', 'daily_budget'])['targeting']._json
        print('targeting spec:\n%s\n\n\n'%targeting_spec)
        if targeting_spec not in major_dict.keys():
          major_dict[targeting_spec] = []
          major_dict[targeting_spec].append(adset)
        elif targeting_spec in major_dict.keys():
          major_dict[targeting_spec].append(adset)

      targeting_spec_count = len(major_dict.keys())
      print("targeting spec count: %s" % targeting_spec_count)
      for targeting_spec, adsets in major_dict.items():
        current_budget_list = sorted(list(map(int, key('daily_budget', adsets))), reverse=False)
        print("current budget list: %s" % current_budget_list)

        original_adset = None
        roi_list = []
        for adset in adsets:
          if adset['daily_budget'] == "500":
            original_adset = adset
          for csv_adset in csv_adsets:
            if csv_adset['Ad Set ID'] == adset['id']:
              roi_list.append(csv_adset['roi'])

        print("original_adset: %s" % original_adset['id'])
        print("roi_list: %s, count: %s" % (roi_list, len(roi_list)))

        count_of_good_rois = len([i for i in roi_list if i > 2])
        print("count of good rois: %s" % count_of_good_rois)
        new_budgets = list(range(max(current_budget_list) + 500, 40000, 500))[:count_of_good_rois]    
        print("new rois: %s" % new_budgets)


        for new_budget in new_budgets:
          try:
            new_adset, new_ad = Copy(shop, original_adset['id'])
            print("making a copy")
            new_adset['daily_budget'] = new_budget
            new_adset.remote_read(fields=['name', 'start_time', 'effective_status', ])
            new_adset.remote_update()
            print('new adset: %s\n' % new_adset)
            time.sleep(12)
            count_of_newly_created_adsets += 1
            sum_of_newly_created_adsets_budget += new_budget
          except:
            errors+=1
    print("error with duplication count is: %s"%errors)


    print('\n\n\n\n\n')
    print("sum of current_budget_today: %s" % (sum(list(map(int, key(csv_adsets, 'Budget'))))))
    print("sum of current_budget_today spent so far: %s" % (sum(list(map(float, key(csv_adsets, 'Amount Spent (USD)'))))))
    print("sum of purchases value today so far: %s" % (sum(list(map(float, key(csv_adsets, 'Website Purchases Conversion Value'))))))
    print("sum of purchases value target today: %s" % (sum(list(map(int, key(csv_adsets, 'Budget')))) * 2))
    print("count of newly created adsets: %s" % count_of_newly_created_adsets)
    print("sum of newly created adsets budgets: %s" % sum_of_newly_created_adsets_budget)
    print('\n\n\n\n\n')
    print('-'*20)
  def Copy(id,**kwargs):
    # v3.3
    return [setitem(kwargs,"x",list(map(Integer,key("copied_id", [Shop()(All(Shop)[0].shop_abbreviation),json.loads(requests.post("https://graph.facebook.com/v3.3/%s/copies"%id, data={ "deep_copy":"true",
                 "start_time":"%s 6:00:00 EST"%(Date().dt(0) if datetime.now().hour in [0,1,2] else Date().dt(1)),
                 "status_option": "ACTIVE",
                 "access_token": Shop.objects.all()[0].Facebook_Business_App_Token, }).content.decode())][1]["ad_object_ids"]))) ),
          [[AdSet(kwargs["x"][0]).remote_update(params={"status":"ACTIVE"}),Ad(kwargs["x"][1]).remote_update(params={"status":"ACTIVE"}),] if(2==len(kwargs["x"])) else [Campaign(kwargs["x"][0]).remote_update(params={"status":"ACTIVE"}),AdSet(kwargs["x"][1]).remote_update(params={"status":"ACTIVE"}),Ad(kwargs["x"][2]).remote_update(params={"status":"ACTIVE"}),] ],
          kwargs["x"],
    ][2]
  def _ads_utils_daily_restart(adsets):
    # ads_utils_restart_if_sale_in_last_20_spent
    # get_adm_url_by_ids(shop, id_list=restart_ids, date_range=180)
    # Directions: Just get_adm_url, and hit 'turn on'
    # delivery, inactive, go to ads, set bd-> daily, sort adname
    # ads_util_restart_adsets(id_list=restart_ids)

    if len(adsets) == 0:
      return
    adset_ids = key(adsets, key='Ad Set ID')
    
    # dict with key as adset_id
    data = dict(zip(adset_ids, [[] for i in range(len(adset_ids))]))
    # dict with values as all days with that adset_id
    for i in adsets:
      i['date'] = Date(i['Reporting Starts']).dateobj
    for a in data:
      for i in adsets:
        if i['Ad Set ID'] == a:
          data[a].append(i)
    # sort adsets based on date ordered past to future
    # sets spent, purchases, num_consec_bad to 0,0,0
    # for each adset_id, for each day in the value list, adds the spent, purchases.
    # if spent >20, purchases == 0, no matter the day, it is a bad consecutive adset.
    # if it is bad, sets spent, purchases, to 0,0 to restart count & not overlap
    # assigns num_consec_bad to adset's dict.
    for a in data:
      data[a] = keysort('date', data[a], tcer=False)
    for k,v in data.items():
      spent = 0
      purchases = 0
      num_consec_bad = 0
      for adset in v:
        spent += float(adset['Amount Spent (USD)'])
        purchases += float(adset['Website Purchases'])
        #print(spent, purchases)
        if spent > 20 and purchases == 0:
          num_consec_bad += 1
          purchases = 0
          spent = 0
        adset['num_consec_bad'] = num_consec_bad
      print('Ad Set ID: %s | num_consec_bad: %s' % (adset['Ad Set ID'], adset['num_consec_bad']))
    # sorts adsets ordered now to backthen
    # if num_consec_bad is > 3, do not restart
    # otherwise, counts from date now to backthen, if has purchase in last 20 spent, add to restart_id list.
    for a in data:
      data[a] = keysort('date', data[a], tcer=True)
    restart_ids = []
    for k,v in data.items():
      day = 0
      spent = 0
      purchases = 0
      for adset in v:
        day += 1
        spent += float(adset['Amount Spent (USD)'])
        purchases += float(adset['Website Purchases'])
        print("date: %s, spent: %s, pcs: %s" % (adset['date'], adset['Amount Spent (USD)'], adset['Website Purchases']))
        if day <= 4 and spent <= 20 and purchases > 0:
          if adset['num_consec_bad'] <= 2:
            print("will be restarted... ")
            restart_ids.append(int(adset['Ad Set ID'].replace('c:','')))
      print("\n\n\n")
    restart_ids = list(set(restart_ids))
    for _id in restart_ids:
      print("RESTART_IDS: %s"%_id)
    #get_adm_url_by_ids(shop, restart_ids, action='restart')
    _ads_utils_restart_adsets(list(set(restart_ids)))
  def _ads_utils_daily_stop(adsets):
    if len(adsets) == 0:
      return
    print(""" If you want to check against it, generate list of pause_ids, 
              filter-> delivery: active,&go to ads,& set bd->daily,& sort adname.""")
    for i in adsets:
      i['id_'] = i['Ad Set ID'].replace('c:','')
      i['date'] = Date(i['Reporting Starts']).dateobj
    pause_ids = []
    adset_ids = list(set(key(adsets, key='id_')))
    for id in adset_ids:
      sorted_ads = keysort('date', keyequals('id_', id, adsets), tcer=True)
      spent = 0
      pcs = 0
      print('id: %s' % id)
      for adset in sorted_ads:
        spent += float(adset['Amount Spent (USD)'])
        pcs += float(adset['Website Purchases'])
        print("date: %s, spent: %s, pcs: %s" % (adset['date'], adset['spent'], adset['pcs']))
        if (spent >= 20 and pcs == 0):
          print("spend over 20: %s" % (spent - 20))
          pause_id = adset['id_']
          if pause_id not in pause_ids:
            pause_ids.append(pause_id)
            print("will be paused.")
      print('\n\n')
      time.sleep(8)

    _ads_utils_pause_adsets(pause_ids)


    #get_adm_url_by_ids(shop, pause_ids, action='pause')
    _ads_utils_pause_adsets(list(set(pause_ids)))
  def _ads_utils_pause_adsets(id_list):
    id_list = list(set(id_list))
    for adset_id in list(set(id_list)):
      adset = AdSet(adset_id)
      adset['status'] = 'PAUSED'
      status_check = adset.remote_update()
      print("adset %s: %s √"%(adset_id, status_check))
      assert status_check['status'] == 'PAUSED'
      ad = adset.get_ads()[0]
      ad['status'] = "PAUSED"
      status_check = ad.remote_update()
      assert status_check['status'] == 'PAUSED'
      print("ad %s: %s √" % (ad['id'], status_check))
      print('\n\n')
      time.sleep(10)
      # tested and works
  def _ads_utils_restart_adsets(id_list):
    for adset_id in id_list:
      adset = AdSet(adset_id)
      adset['status'] = 'ACTIVE'
      status_check = adset.remote_update()
      print("%s: %s √"%(adset_id, status_check))
      assert status_check['status'] == 'ACTIVE'
      ad = adset.get_ads()[0]
      ad["status"] = "ACTIVE"
      status_check = ad.remote_update()
      assert status_check['status'] == "ACTIVE"
      print("ad %s: %s √" % (ad['id'], status_check))
      print('\n\n')
      time.sleep(10)
      # tested and works
  def _create_custom(handle, shop):
    print("...Creating Custom...")
    audience = CustomAudience(parent_id='act_%s' %shop.Facebook_Business_Ad_Account_ID); zz(12)
    print("Creating %s for handle: %s"%(audience, handle))
    params={'pixel_id': shop.Facebook_Pixel_ID,'subtype':'WEBSITE','retention_days':'180',
        'rule':{"url":{"i_contains": handle}}, 'name':handle,}
    custom = audience.remote_create(params=params)['id']
    print("Successfully Created Custom Audience... \n%s"%custom)
    return custom
  def adjust_ad_columns():
    pyperclip.copy('x = document.getElementsByTagName("div")\ny = []\nz = x.length\nfor (i=0;i<z;i++) {a=x[i]; if (a.getAttribute("data-testid")=="FixedDataTableRow") {y=y.concat(a);}}\nb = y.length\nfor (i=0;i<b;i++) {\n                    a = y[i];\n                    c = a.getElementsByClassName("_4h2m");\n                    console.log(c.length);\n                    d = c[0]; d.style.width = "40px"; d.style.left = "0px";\n                    d = c[1]; d.style.width = "40px"; d.style.left = "40px";\n                    d = c[2]; d.style.width = "160px"; d.style.left = "80px";\n                    d = c[3]; d.style.width = "100px"; d.style.left = "0px";\n                    d = c[4]; d.style.width = "100px"; d.style.left = "100px";\n                    d = c[5]; d.style.width = "100px"; d.style.left = "200px";\n                    d = c[6]; d.style.width = "100px"; d.style.left = "300px";\n                    d = c[7]; d.style.width = "100px"; d.style.left = "400px";\n                    d = c[8]; d.style.width = "100px"; d.style.left = "500px";\n                    d = c[9]; d.style.width = "100px"; d.style.left = "600px";\n                    d = c[10]; d.style.width = "100px"; d.style.left = "700px";\n                    d = c[11]; d.style.width = "100px"; d.style.left = "800px";\n                    d = c[12]; d.style.width = "100px"; d.style.left = "900px";\n                    d = c[13]; d.style.width = "100px"; d.style.left = "1000px";\n                    d = c[14]; d.style.width = "100px"; d.style.left = "1100px";\n                    d = c[15]; d.style.width = "100px"; d.style.left = "1200px";\n                    d = c[16]; d.style.width = "100px"; d.style.left = "1300px";\n                    d = c[17]; d.style.width = "100px"; d.style.left = "1400px";\n                    e = a.getElementsByClassName("_3pzk");\n                    f = e[1]; f.style.width = "241px"; f.style.left = "241px";\n}\nx = document.getElementsByClassName("_1mic")[0];\ny = x.getElementsByClassName("_4h2m");\nz = y[0]; z.style.width = "40px"; z.style.left = "0px";\nz = y[1]; z.style.width = "40px"; z.style.left = "40px";\nz = y[2]; z.style.width = "160px"; z.style.left = "80px";\nz = y[3]; z.style.width = "100px"; z.style.left = "0px";\nz = y[4]; z.style.width = "100px"; z.style.left = "100px";\nz = y[5]; z.style.width = "100px"; z.style.left = "200px";\nz = y[6]; z.style.width = "100px"; z.style.left = "300px";\nz = y[7]; z.style.width = "100px"; z.style.left = "400px";\nz = y[8]; z.style.width = "100px"; z.style.left = "500px";\nz = y[9]; z.style.width = "100px"; z.style.left = "600px";\nz = y[10]; z.style.width = "100px"; z.style.left = "700px";\nz = y[11]; z.style.width = "100px"; z.style.left = "800px";\nz = y[12]; z.style.width = "100px"; z.style.left = "900px";\nz = y[13]; z.style.width = "100px"; z.style.left = "1000px";\nz = y[14]; z.style.width = "100px"; z.style.left = "1100px";\nz = y[15]; z.style.width = "100px"; z.style.left = "1200px";\nz = y[16]; z.style.width = "100px"; z.style.left = "1300px";\nz = y[17]; z.style.width = "100px"; z.style.left = "1400px";\ne = x.getElementsByClassName("_3pzk");\nf = e[1]; f.style.width = "241px"; f.style.left = "241px";\n\nx = document.getElementsByClassName("_1mme")[0];\ny = x.getElementsByClassName("_1eyi");\nz = y[0]; z.style.width = "40px"; z.style.left = "0px";\nz = y[1]; z.style.width = "40px"; z.style.left = "40px";\nz = y[2]; z.style.width = "160px"; z.style.left = "80px";\nz = y[3]; z.style.width = "100px"; z.style.left = "0px";\nz = y[4]; z.style.width = "100px"; z.style.left = "100px";\nz = y[5]; z.style.width = "100px"; z.style.left = "200px";\nz = y[6]; z.style.width = "100px"; z.style.left = "300px";\nz = y[7]; z.style.width = "100px"; z.style.left = "400px";\nz = y[8]; z.style.width = "100px"; z.style.left = "500px";\nz = y[9]; z.style.width = "100px"; z.style.left = "600px";\nz = y[10]; z.style.width = "100px"; z.style.left = "700px";\nz = y[11]; z.style.width = "100px"; z.style.left = "800px";\nz = y[12]; z.style.width = "100px"; z.style.left = "900px";\nz = y[13]; z.style.width = "100px"; z.style.left = "1000px";\nz = y[14]; z.style.width = "100px"; z.style.left = "1100px";\nz = y[15]; z.style.width = "100px"; z.style.left = "1200px";\nz = y[16]; z.style.width = "100px"; z.style.left = "1300px";\nz = y[17]; z.style.width = "100px"; z.style.left = "1400px";\ne = x.getElementsByClassName("_182x");\nf = e[1]; f.style.left = "241px";\n\n\nx = document.getElementsByClassName("_1mme")[0];\ny = x.getElementsByClassName("_4h2m");\nz = y[0]; z.style.width = "40px";\nz = y[1]; z.style.width = "40px";\nz = y[2]; z.style.width = "160px";\nz = y[3]; z.style.width = "100px";\nz = y[4]; z.style.width = "100px";\nz = y[5]; z.style.width = "100px";\nz = y[6]; z.style.width = "100px";\nz = y[7]; z.style.width = "100px";\nz = y[8]; z.style.width = "100px";\nz = y[9]; z.style.width = "100px";\nz = y[10]; z.style.width = "100px";\nz = y[11]; z.style.width = "100px";\nz = y[12]; z.style.width = "100px";\nz = y[13]; z.style.width = "100px";\nz = y[14]; z.style.width = "100px";\nz = y[15]; z.style.width = "100px";\nz = y[16]; z.style.width = "100px"; z.style.left = "1300px";\nz = y[17]; z.style.width = "100px"; z.style.left = "1400px";\ne = x.getElementsByClassName("_3pzk");\nf = e[1]; f.style.width = "241px"; f.style.left = "241px";\n')
    while True:
      chromejs("x = document.getElementsByTagName('div');y = [];z = x.length;for (i=0;i<z;i++) {a=x[i]; if (a.getAttribute('data-testid')=='FixedDataTableRow') {y=y.concat(a);}};b = y.length; for (i=0;i<b;i++) {a = y[i];c = a.getElementsByClassName('_4h2m');console.log(c.length);d = c[0]; d.style.width = '40px'; d.style.left = '0px';d = c[1]; d.style.width = '40px'; d.style.left = '40px';d = c[2]; d.style.width = '160px'; d.style.left = '80px';d = c[3]; d.style.width = '100px'; d.style.left = '0px';d = c[4]; d.style.width = '100px'; d.style.left = '100px';d = c[5]; d.style.width = '100px'; d.style.left = '200px';d = c[6]; d.style.width = '100px'; d.style.left = '300px';d = c[7]; d.style.width = '100px'; d.style.left = '400px';d = c[8]; d.style.width = '100px'; d.style.left = '500px';d = c[9]; d.style.width = '100px'; d.style.left = '600px';d = c[10]; d.style.width = '100px'; d.style.left = '700px';d = c[11]; d.style.width = '100px'; d.style.left = '800px';d = c[12]; d.style.width = '100px'; d.style.left = '900px';d = c[13]; d.style.width = '100px'; d.style.left = '1000px';d = c[14]; d.style.width = '100px'; d.style.left = '1100px';d = c[15]; d.style.width = '100px'; d.style.left = '1200px';d = c[16]; d.style.width = '100px'; d.style.left = '1300px';d = c[17]; d.style.width = '100px'; d.style.left = '1400px';e = a.getElementsByClassName('_3pzk');f = e[1]; f.style.width = '241px'; f.style.left = '241px';}; x = document.getElementsByClassName('_1mic')[0]; y = x.getElementsByClassName('_4h2m'); z = y[0]; z.style.width = '40px'; z.style.left = '0px'; z = y[1]; z.style.width = '40px'; z.style.left = '40px'; z = y[2]; z.style.width = '160px'; z.style.left = '80px'; z = y[3]; z.style.width = '100px'; z.style.left = '0px'; z = y[4]; z.style.width = '100px'; z.style.left = '100px'; z = y[5]; z.style.width = '100px'; z.style.left = '200px'; z = y[6]; z.style.width = '100px'; z.style.left = '300px'; z = y[7]; z.style.width = '100px'; z.style.left = '400px'; z = y[8]; z.style.width = '100px'; z.style.left = '500px'; z = y[9]; z.style.width = '100px'; z.style.left = '600px'; z = y[10]; z.style.width = '100px'; z.style.left = '700px'; z = y[11]; z.style.width = '100px'; z.style.left = '800px'; z = y[12]; z.style.width = '100px'; z.style.left = '900px'; z = y[13]; z.style.width = '100px'; z.style.left = '1000px'; z = y[14]; z.style.width = '100px'; z.style.left = '1100px'; z = y[15]; z.style.width = '100px'; z.style.left = '1200px'; z = y[16]; z.style.width = '100px'; z.style.left = '1300px'; z = y[17]; z.style.width = '100px'; z.style.left = '1400px'; e = x.getElementsByClassName('_3pzk'); f = e[1]; f.style.width = '241px'; f.style.left = '241px'; x = document.getElementsByClassName('_1mme')[0]; y = x.getElementsByClassName('_1eyi'); z = y[0]; z.style.width = '40px'; z.style.left = '0px'; z = y[1]; z.style.width = '40px'; z.style.left = '40px'; z = y[2]; z.style.width = '160px'; z.style.left = '80px'; z = y[3]; z.style.width = '100px'; z.style.left = '0px'; z = y[4]; z.style.width = '100px'; z.style.left = '100px'; z = y[5]; z.style.width = '100px'; z.style.left = '200px'; z = y[6]; z.style.width = '100px'; z.style.left = '300px'; z = y[7]; z.style.width = '100px'; z.style.left = '400px'; z = y[8]; z.style.width = '100px'; z.style.left = '500px'; z = y[9]; z.style.width = '100px'; z.style.left = '600px'; z = y[10]; z.style.width = '100px'; z.style.left = '700px'; z = y[11]; z.style.width = '100px'; z.style.left = '800px'; z = y[12]; z.style.width = '100px'; z.style.left = '900px'; z = y[13]; z.style.width = '100px'; z.style.left = '1000px'; z = y[14]; z.style.width = '100px'; z.style.left = '1100px'; z = y[15]; z.style.width = '100px'; z.style.left = '1200px'; z = y[16]; z.style.width = '100px'; z.style.left = '1300px'; z = y[17]; z.style.width = '100px'; z.style.left = '1400px'; e = x.getElementsByClassName('_182x'); f = e[1]; f.style.left = '241px'; x = document.getElementsByClassName('_1mme')[0]; y = x.getElementsByClassName('_4h2m'); z = y[0]; z.style.width = '40px'; z = y[1]; z.style.width = '40px'; z = y[2]; z.style.width = '160px'; z = y[3]; z.style.width = '100px'; z = y[4]; z.style.width = '100px'; z = y[5]; z.style.width = '100px'; z = y[6]; z.style.width = '100px'; z = y[7]; z.style.width = '100px'; z = y[8]; z.style.width = '100px'; z = y[9]; z.style.width = '100px'; z = y[10]; z.style.width = '100px'; z = y[11]; z.style.width = '100px'; z = y[12]; z.style.width = '100px'; z = y[13]; z.style.width = '100px'; z = y[14]; z.style.width = '100px'; z = y[15]; z.style.width = '100px'; z = y[16]; z.style.width = '100px'; z.style.left = '1300px'; z = y[17]; z.style.width = '100px'; z.style.left = '1400px'; e = x.getElementsByClassName('_3pzk'); f = e[1]; f.style.width = '241px'; f.style.left = '241px';")
      time.sleep(0.2)
  def adsFeed(self, date_range=100, bd=True, filters=None):
    print("FEEDING ADSETS")
    self.ff = Browser()("sele", window_index=[0,0,4,4])
    url = format_url(self, date_range, bd, filters)
    self.ff.get(url)
    self.ff.fcss('._2a2d').click(); zz(6)
    try: adms = CSV().DictRead(time_a_download(method=self.ff.ffs('button','action','confirm').click))
    except: adms = CSV().DictRead(time_a_download(method=self.ff.fcn('layerConfirm').click))
    print('adms: %s'%adms)
    if 'No data available' in str(adms):
      print("no adsets")
      return []
    adms = [i for i in adms if i['Ad Set ID'] != '' and i['Ad Set Name'] != None and 'DPA' not in i['Ad Set Name']]
    for adm in adms:
      for a in adm:
        if adm[a] == '' or adm[a] == None:
          adm[a] = 0
      # adm['data'] = eval(adm['Ad Set Name'])
      adm['spent'] = float(adm['Amount Spent (USD)'])
      adm['pcv'] = float(adm['Website Purchases Conversion Value'])
      adm['pcs'] = float(adm['Website Purchases'])
      adm['cpc'] = float(adm['CPC (Cost per Link Click) (USD)'])
      adm['clicks'] = float(adm['Link Clicks'])
      adm['roi'] = float(adm['pcv']) / float(adm['spent']) if adm['spent'] != 0 else 0
    """
    print("...feedAudience...")
    for x in Audience.objects.all():
      x.pcs = 0
      x.roi = 0
      x.spent = 0.01
      x.pcv = 0
      
      matching_audiences = [i for i in adms if i['data']['audname'] == x.name]
      x.pcs += sum(key(matching_audiences, 'pcs'))
      x.spent += sum(key(matching_audiences, 'spent'))
      x.pcv += sum(key(matching_audiences, 'pcv'))
      x.roi += x.pcv / x.spent
      x.save()
    print("...feedProduct...")
    for x in Product.objects.all():
      x.pcs = 0
      x.roi = 0
      x.spent = 0.01
      x.pcv = 0
      
      x.pcs = sum([i['pcs'] for i in adms if i['data']['handle'] == x.handle])
      x.spent += sum([i['spent'] for i in adms if i['data']['handle'] == x.handle])
      x.pcv = sum([i['pcv'] for i in adms if i['data']['handle'] == x.handle])
      x.roi = x.pcv / x.spent
      print(x.pcs, x.spent, x.pcv, x.roi)
      x.save()
    """

    self.adms = adms
    self.ff.quit()
    return self.adms
  def advertise():
    storeabbre = input("what store abbre?: ")
    shop = Shop()( storeabbre)
    BASE_ADSET_DICTIONARY = {'Ad ID': '','Ad Name': 'test','Ad Set Daily Budget': '5','Ad Set ID': '','Ad Set Lifetime Budget': '0','Ad Set Lifetime Impressions': '0','Ad Set Name': 'test','Ad Set Run Status': 'ACTIVE','Ad Set Schedule': '','Ad Set Time Start': '%s 2:00:00 am' % Date().dt(1, '%m/%d/%Y'),'Ad Set Time Stop': '','Ad Status': 'ACTIVE','Add End Card': '','Additional Custom Tracking Specs': '[]','Addresses': '','Age Max': '65','Age Min': '18','Android App Name': '','Android Package Name': '','App Destination': '','Application ID': '','Attribution Spec': '[{"event_type":"CLICK_THROUGH","window_days":7},{"event_type":"VIEW_THROUGH","window_days":1}]','Audience Network Positions': 'classic','Automatically Set Bid': 'Yes','Behaviors': '','Bid Amount': '','Billing Event': 'IMPRESSIONS','Body': '','Broad Category Clusters': '','Buying Type': 'AUCTION','Call to Action': '','Call to Action Link': '','Campaign ID': '','Campaign KPI': '','Campaign KPI Custom Conversion ID': '','Campaign Name': 'test','Campaign Objective': 'Conversions','Campaign Page ID': '','Campaign Spend Limit': '','Campaign Status': 'ACTIVE','Cities': '','College End Year': '','College Start Year': '','Connections': '','Conversion Tracking Pixels': 'tp:141019342913259','Countries': 'US','Creative Optimization': '','Creative Type': 'Photo Page Post Ad','Custom Audiences': '','Deep Link For Android': '','Deep Link For Windows Phone': '','Deep Link For iOS': '','Deep Link For iPad': '','Deep Link For iPhone': '','Deep link to website': '','Destination Type': 'UNDEFINED','Device Platforms': 'mobile, desktop','Display Link': '','Dynamic Ad Voice': '','Education Schools': '','Education Status': '','Electoral Districts': '','Event ID': '','Excluded Addresses': '','Excluded Cities': '','Excluded Connections': '','Excluded Countries': '','Excluded Custom Audiences': '','Excluded Electoral Districts': '','Excluded Geo Markets (DMA)': '','Excluded Global Regions': '','Excluded Product Audience Specs': '','Excluded Publisher Categories': '','Excluded Regions': '','Excluded User AdClusters': '','Excluded User Device': '','Excluded Zip': '','Facebook App ID': '','Facebook Positions': 'feed, right_hand_column','Family Statuses': '','Fields of Study': '','Flexible Exclusions': '','Flexible Inclusions': '[{"interests":[{"id":"6003324061606","name":"Audrey Hepburn"},{"id":"6003347600674","name":"Katharine Hepburn"},{"id":"6003392991271","name":"Rockabilly"},{"id":"6011957502962","name":"www.rockabilly-clothing.de"},{"id":"6013806088087","name":"Viva Las Vegas Rockabilly Weekend"}]}]','Force Single Link': '','Frequency Control': '','Friends of Connections': '','Gender': '','Generation': '','Geo Markets (DMA)': '','Global Regions': '','Home Ownership': '','Home Type': '','Home Value': '','Household Composition': '','Image': '83824348246.jpg','Image Crops': '','Image Hash': '','Image Overlay Float With Margin': '','Image Overlay Position': '','Image Overlay Template': '','Image Overlay Text Font': '','Image Overlay Text Type': '','Image Overlay Theme Color': '','Income': '','Industries': '','Instagram Account ID': '','Instagram Platform Image Crops': '','Instagram Platform Image Hash': '','Instagram Platform Image URL': '','Instagram Positions': '','Instagram Preview Link': '','Interested In': '','Lead Form ID': '','Life Events': '','Link': 'https://www.facebook.com/steampunkstop/photos/p.1998717263718262/1998717263718262/?type=3','Link Description': 'Auxiliary. We’ve Scourged Hotspots Of The Earth Mercilessly With Grandiose Detectors And Finally Our SteamBots Have Enchanted The Auxiliary Dress With Magnetic Seals To Affix Protection Spirits To It Permanently.\nClick Below 👇\nsteampunkstop.com/auxiliary','Link Object ID': 'o:1669573053299353','Locales': '','Location Types': 'home, recent','Messenger Positions': '','Mobile App Deep Link': '','Moms': '','Multicultural Affinity': '','Net Worth': '','Object Store URL': '','Offer ID': '','Office Type': '','Optimization Goal': 'OFFSITE_CONVERSIONS','Optimized Conversion Tracking Pixels': 'tp:141019342913259','Optimized Custom Conversion ID': '','Optimized Event': 'PURCHASE','Optimized Pixel Rule': '','Page Welcome Message': '','Permalink': 'https://business.facebook.com/1669573053299353/posts/1998717263718262?business_id=560484760766872','Place Page Set ID': '','Politics': '','Post Click Item Description': '','Post Click Item Headline': '','Preview Link': 'https://www.facebook.com/?feed_demo_ad=6095601486324&h=AQDKS_Ci6KEDEOCa','Product 1 - Description': '','Product 1 - Display Link': '','Product 1 - Image Crops': '','Product 1 - Image Hash': '','Product 1 - Is Static Card': '','Product 1 - Link': '','Product 1 - Mobile App Deep Link': '','Product 1 - Name': '','Product 1 - Place Data': '','Product 1 - Video ID': '','Product 10 - Description': '','Product 10 - Display Link': '','Product 10 - Image Crops': '','Product 10 - Image Hash': '','Product 10 - Is Static Card': '','Product 10 - Link': '','Product 10 - Mobile App Deep Link': '','Product 10 - Name': '','Product 10 - Place Data': '','Product 10 - Video ID': '','Product 2 - Description': '','Product 2 - Display Link': '','Product 2 - Image Crops': '','Product 2 - Image Hash': '','Product 2 - Is Static Card': '','Product 2 - Link': '','Product 2 - Mobile App Deep Link': '','Product 2 - Name': '','Product 2 - Place Data': '','Product 2 - Video ID': '','Product 3 - Description': '','Product 3 - Display Link': '','Product 3 - Image Crops': '','Product 3 - Image Hash': '','Product 3 - Is Static Card': '','Product 3 - Link': '','Product 3 - Mobile App Deep Link': '','Product 3 - Name': '','Product 3 - Place Data': '','Product 3 - Video ID': '','Product 4 - Description': '','Product 4 - Display Link': '','Product 4 - Image Crops': '','Product 4 - Image Hash': '','Product 4 - Is Static Card': '','Product 4 - Link': '','Product 4 - Mobile App Deep Link': '','Product 4 - Name': '','Product 4 - Place Data': '','Product 4 - Video ID': '','Product 5 - Description': '','Product 5 - Display Link': '','Product 5 - Image Crops': '','Product 5 - Image Hash': '','Product 5 - Is Static Card': '','Product 5 - Link': '','Product 5 - Mobile App Deep Link': '','Product 5 - Name': '','Product 5 - Place Data': '','Product 5 - Video ID': '','Product 6 - Description': '','Product 6 - Display Link': '','Product 6 - Image Crops': '','Product 6 - Image Hash': '','Product 6 - Is Static Card': '','Product 6 - Link': '','Product 6 - Mobile App Deep Link': '','Product 6 - Name': '','Product 6 - Place Data': '','Product 6 - Video ID': '','Product 7 - Description': '','Product 7 - Display Link': '','Product 7 - Image Crops': '','Product 7 - Image Hash': '','Product 7 - Is Static Card': '','Product 7 - Link': '','Product 7 - Mobile App Deep Link': '','Product 7 - Name': '','Product 7 - Place Data': '','Product 7 - Video ID': '','Product 8 - Description': '','Product 8 - Display Link': '','Product 8 - Image Crops': '','Product 8 - Image Hash': '','Product 8 - Is Static Card': '','Product 8 - Link': '','Product 8 - Mobile App Deep Link': '','Product 8 - Name': '','Product 8 - Place Data': '','Product 8 - Video ID': '','Product 9 - Description': '','Product 9 - Display Link': '','Product 9 - Image Crops': '','Product 9 - Image Hash': '','Product 9 - Is Static Card': '','Product 9 - Link': '','Product 9 - Mobile App Deep Link': '','Product 9 - Name': '','Product 9 - Place Data': '','Product 9 - Video ID': '','Product Audience Specs': '','Product Catalog ID': '','Product Link': '','Product Set ID': '','Publisher Platforms': 'facebook, audience_network','Rate Card': '','Regions': '','Relationship': '','Retailer IDs': '','Site Category': '','Story ID': '','Tags': '','Targeted Business Locations': '','Targeting Categories - ALL OF': '','Targeting Optimization': '','Template URL': '','Title': '','URL Tags': '','Unified Interests': '','Use Accelerated Delivery': 'No','Use Average Bid': 'No','Use Page as Actor': 'No','User Device': '','User OS Version': '','User Operating System': '','Video ID': '','Video Retargeting': 'No','Video Thumbnail URL': '','Windows App Name': '','Windows Store ID': '','Wireless Carrier': '','Work Employers': '','Work Job Titles': '','Zip': '','iOS App Name': '','iOS App Store ID': '','iPad App Name': '','iPad App Store ID': '','iPhone App Name': '','iPhone App Store ID': ''}




    DICTIONARYS_FOR_CSV = []






    products_csv=os.path.expanduser('~/tavern/tavern/products.csv')
    PRODUCTS_ROWS_DICTIONARYS = CSV().DictRead(products_csv)


    products = productsFeed(shop)
    FULL_EXTENSION_FILENAMES = []
    for ROW in PRODUCTS_ROWS_DICTIONARYS:

      if ROW["advertise?"] == "TRUE":
        p = [i for i in products if i["title"] == ROW["title"]][-1]
        p = shop.shopify.Product.find(id_=p['id'])




        caption = create_caption(p, shop, ROW['caption'], ROW["shopify_url"])



        NEW_DATA = copy.deepcopy(BASE_ADSET_DICTIONARY)
        NEW_DATA["Flexible Inclusions"] = ""
        NEW_DATA['Campaign Name'] = p.handle
        NEW_DATA['Ad Set Name'] = caption.replace("\n", " ")
        NEW_DATA['Ad Name'] = NEW_DATA['Ad Set Name']
        NEW_DATA['Display Link'] = caption
        NEW_DATA['Title'] = caption
        NEW_DATA['Body'] = caption
        NEW_DATA['Post Click Item Headline'] = caption
        NEW_DATA['Description'] = caption

        try:
          variant_id = int(ROW["shopify_url"].split("variant=")[-1])

          print("variant id: %s" )


          ############ FINDING MATCHING IMAGE FROM PRODUCT IMAGES BASED ON VARIANT ID

          img_id = None
          for i in p.variants:
            if i.id == variant_id:
              img_id = i.image_id
              print("Found matching img_id to URL %s" % url)
          variant_src = None
          for i in p.images:
            if i.id == img_id:
              variant_src = i.src
              print("Found matching variant_id to img_id.. %s" % variant_src)
          fn = None
          if variant_src is not None:
            fn = Images().download_and_resize(variant_src, 1200)
          if img_id is None: # this is in the case its a "1 Title Product"
            fn = Images().download_and_resize(p.image.src, 1200)
          print("image filename for the variant: %s" % fn)
          FULL_EXTENSION_FILENAMES.append(fn)
          NEW_DATA['Image'] = fn.split('/')[-1]

          pprint(NEW_DATA)

          DICTIONARYS_FOR_CSV.append(NEW_DATA)
        except Exception as e:
          print("error with possibly probably - the product has 0 variants and thus variantless URL, error:\n%s"% e )




    tmp_file = os.path.expanduser("~/tmp.csv")
    CSV().DictWrite(tmp_file, DICTIONARYS_FOR_CSV)

    ss = Browser()("sele")
    if not Get(Shop,shop_abbreviation=Muta()().store_abbre).Facebook_Business_Manager_ID:
      Update(Get(Shop,shop_abbreviation=Muta()().store_abbre),Facebook_Business_Manager_ID=OSA.log("Enter in the Facebook Business Manager ID. You can usually find it in the url like business_id=<Business ID>."))

    ss.get("https://business.facebook.com/ads/manage/powereditor/manage/campaigns?act={}&business_id={}&columns=start_time%2Ccampaign_group_name%2Cname%2Ccampaign_id%2Cimpressions%2Cfrequency%2Ccpm%2Cclicks%2Cctr%2Cactions%3Alink_click%2Ccost_per_action_type%3Alink_click%2Cspend%2Caction_values%3Aoffsite_conversion.fb_pixel_purchase%2Cactions%3Aoffsite_conversion.fb_pixel_purchase%2Ccost_per_action_type%3Aoffsite_conversion.fb_pixel_purchase%2Cactions%3Aoffsite_conversion.checkout%2Ccost_per_action_type%3Aoffsite_conversion.checkout%2Cbudget%2Crelevance_score%3Ascore%2Cwebsite_purchase_roas%3Aoffsite_conversion.fb_pixel_purchase&attribution_windows=default&date=2005-02-01_2017-12-31%2Clifetime".format(Get(Shop,shop_abbreviation=Muta()().store_abbre).Facebook_Business_Ad_Account_ID, Get(Shop,shop_abbreviation=Muta()().store_abbre).Facebook_Business_Manager_ID))
    
    #""" # OLD WITH FIREFOX
    try:
      ss.ffs('button','data-tooltip-content','Create & Edit in a Spreadsheet').click()
    except:
      ss.ffs('button','data-tooltip-content','Export & import').click()
    ss.ffss('li','role','presentation')[-2].click()
    ss.ffs('input','data-testid','import-paste-text-link').send_keys(tmp_file)
    IMAGE_UPLOAD_BUTTON = ss.ffs('input','accept','image/jpg, image/jpeg, image/gif, image/bmp, image/png, image/tiff, image/tif')

    for x in FULL_EXTENSION_FILENAMES:
      IMAGE_UPLOAD_BUTTON.send_keys(x)


    ss.ffs('button','data-testid','import-button').click()
    #"""
    while True:
      if "Your import is complete" in ss.page_source:
        time.sleep(3)
        break
    ss.quit()
    # advertise(url, p, caption)
  def alter_redirect(shop_abbreviation, previous_path, new_path, new_target):
    redirects = get_redirects(Shop()(shop_abbreviation))
    redirect = [i for i in redirects if i.path == previous_path][0]
    redirect.path = new_path
    redirect.target = new_target
    assert True == redirect.save()
    assert requests.get("%s%s"%(Shop()(shop_abbreviation).Domain_Name,new_path)).url==new_target
  def caption_tee():
    caption_to_tee = multi_input("caption to tee: ")
    os.system("echo '============================\n%s\n\n============================' | tee -a ./.teed_captions.txt" % caption_to_tee)
  def check_remaining():
    page_name = OSA.log("Page name?")
    OSA.log("%s"%(len(get_scheduled_posts(page_name))))
  def cloaker(io=None, direction=None):
    """ ::: Initiate Shop ::: """
    a_shop()
    """ ::: If you use July_Adset_Utilities to update all adset targeting data, to ::: """
    """ ::: Get the most accurate adset effective_status data, it's the same as ::: """
    """ ::: requesting all adset_ids in database, checking if active status, (to change adset name)::: """
    """ ::: So here I update adset targeting data  ///actually at direction==1.\\\::: """
    if direction == 0:
      import builtins
      if type(io) == builtins.dict:
        for adset_id,adset_name in io.items():
          AdSet(adset_id).remote_update(params={"name":adset_name})
          magentaprint(AdSet(adset_id).remote_read(fields=["name"])._json)
    elif direction == 1:
      July_Adset_Utilities().update_adset_targeting_data()
      dict = {}
      for adset in Filter(Adset,status="ACTIVE"):
        name = None
        try:
          name = AdSet(adset.adset_id).remote_read(fields=["name"])._json["name"]
        except Exception as e:
          redprint(e)
          continue
        redprint(adset.adset_id, name)
        dict[adset.adset_id] = name
        AdSet(adset.adset_id).remote_update(params={"name":"0000"})
      return dict
  def createCreative(shop, fn, fb_page_id, caption):
    image = AdImage(parent_id='act_%s'%shop.Facebook_Business_Ad_Account_ID)
    image[AdImage.Field.filename] = fn
    image.remote_create()
    # Output image Hash
    print("hash: %s" % image[AdImage.Field.hash])
    photo_data = AdCreativePhotoData()
    photo_data['image_hash'] = image['hash']
    photo_data['caption'] = caption
    object_story_spec = AdCreativeObjectStorySpec()
    object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = fb_page_id
    object_story_spec[AdCreativeObjectStorySpec.Field.photo_data] = photo_data
    creative = AdCreative(parent_id='act_%s'%shop.Facebook_Business_Ad_Account_ID)
    creative[AdCreative.Field.name] = 'AdCreative %s' % random.randrange(0, 10**10)
    creative[AdCreative.Field.object_story_spec] = object_story_spec
    creative.remote_create()
    print(creative)
    return creative
  def create_ad(product=None,variant_id=None,store_abbre=None,niche=None,page=None,caption=None):
    short_url = create_redirect(Shop()(Muta()().store_abbre), path=("/%s"%(get_handle_from_title(product.title))), target=("%s/products/%s%s"%(Shop()(Muta()().store_abbre).Domain_Name,get_handle_from_title(product.title),("?variant=%s"%(or_list(variant_id,product.variants[0].id)) ))))
    # OSA.log("C")
    caption = caption.replace("<redirect_url>",short_url)
    # OSA.log("D")
    url = None
    if variant_id == None:
      url = product.images[0].src
    else:
      # OSA.log("%s %s"%(variant_id,type(product)))
      # variant = [i for i in product.variants if i.id == variant_id][0]
      # variant_image_id = variant.image_id
      # image = [i for i in product.images if i.id == variant_image_id][0]
      # image_src = image.src
      # if image_src == None:
      #   # 1
      #   image_src = product.images[0].src
      image_src = or_list(lambda:[j.src for j in product.images if j.id == [i for i in product.variants if i.id == variant_id][0]],lambda:product.images[0].src)
      url = image_src
    campaign_id, adset_id = AdsetCreater()(fbid=Shop()(Muta()().store_abbre).Facebook_Business_Ad_Account_ID,url=url,caption=caption,page_id=[i for i in get_pages() if i["name"] == Muta()().page][0]["id"],interest_ids=[])
    # OSA.log("E")
    Save(Adset, campaign_id=campaign_id, adset_id=adset_id, ad_account_id=Shop()(Muta()().store_abbre).Facebook_Business_Ad_Account_ID, is_created=True, handle=product.handle, niche=Muta()().niche, shop_abbreviation=Muta()().store_abbre, facebook_page=Muta()().page, product_url=short_url, image_url=product.images[0].src, caption=caption, interest_ids=[])
    # OSA.log("F")
    Update(product,adset_id=adset_id)
    # OSA.log("G")
    # OSA.log(str(adset_id))
    July_Adset_Utilities().update_advertisement_all(adset_id)
    # OSA.log("H")
  def create_redirect(shop, path, target):
    path = path.lower().strip()
    target = target.lower().strip()

    redirect = shop.shopify.Redirect()
    # redirects = sum([shop.shopify.Redirect.find(status="any", limit=250, page=i) for i in range(1,10)],[])
    redirects = shop.shopify.Redirect.find(path=path)
    if path in key("path", redirects):
      x = [i for i in redirects if i.path == path]
      redirect = x[0]
      print("changing existing redirect of %s to %s"% (redirect.target, target))

    redirect.path = path
    redirect.target = target
    if not redirect.target.startswith("https://"): redirect.target = "https://%s"%redirect.target
    # [3/28/19] https:// required
    assert True == redirect.save()

    distinct_print("%s -----> %s" % (redirect.path, redirect.target))

    x = (shop.Domain_Name + redirect.path).replace("https://","").replace("http://","")
    return x
  def delete_adsets():
    a_shop()
    for i in All(Adset):
      if AdSet(i.adset_id).remote_read(fields=["status"])["status"] == "ARCHIVED":
        print("Deleting one adset")
        Del(i)
        lmap(Del,Filter(Adsetinsight,adset_id=i.adset_id))
  def export_a_video():
    shop, handle = OSA.log("Please enter the shop abbreviation and handle, separated by ', ', [for example: xyz, wall-decal]").split(", ")
    export_address = OSA.log("Please enter the address to export the video to [for example: /Users/user/video.mp4]")
    product = Get(Product,shop=shop,handle=handle)
    video = Get(Video,product_id = product.id)
    open(export_address,"wb").write(video.video)
  def format_url(self, date_range, bd, filters):
    dates = '&date=%s_%s' % (Date().dt(date_range*-1), Date().dt(0))
    day_bd_url = 'https://business.facebook.com/ads/manager/account/adsets/?act='+self.Facebook_Business_Ad_Account_ID+dates+'&time_breakdown=days_1&columns=["start_time"%2C"campaign_group_name"%2C"name"%2C"campaign_id"%2C"impressions"%2C"frequency"%2C"cpm"%2C"clicks"%2C"ctr"%2C"actions%3Alink_click"%2C"cost_per_action_type%3Alink_click"%2C"spend"%2C"action_values%3Aoffsite_conversion.fb_pixel_purchase"%2C"actions%3Aoffsite_conversion.fb_pixel_purchase"%2C"cost_per_action_type%3Aoffsite_conversion.fb_pixel_purchase"%2C"actions%3Aoffsite_conversion.checkout"%2C"cost_per_action_type%3Aoffsite_conversion.checkout"%2C"budget"%2C"relevance_score%3Ascore"]&sort=cost_per_action_type%3Aoffsite_conversion.fb_pixel_purchase~1|delivery_info~1|spent~0|start_time~0&pid=p1'
    if bd==False:
      day_bd_url = day_bd_url.replace('&time_breakdown=days_1', '')
    if filters == 'paused':
      day_bd_url += '&filter_set=[{%22field%22%3A%22campaign.delivery_info%22%2C%22operator%22%3A%22IN%22%2C%22value%22%3A[%22inactive%22]}]'
    if filters == 'active':
      day_bd_url += '&filter_set=[{%22field%22%3A%22campaign.delivery_info%22%2C%22operator%22%3A%22IN%22%2C%22value%22%3A[%22active%22%2C%22limited%22]}]'
    return day_bd_url
  def gen_adset_name(niche,audname,handle,budget)    :
    return str(OrderedDict([('niche',niche), ('audname',audname), ('handle',handle),
                            ('budget',budget) ]))
  def get_next_scheduled_time(page,scheduled_posts):
    times_to_schedule = page.publish_times
    max_scheduled_time = or_list(lambda:max(sud("scheduled_publish_time",scheduled_posts)),lambda:Date()().replace(hour=times_to_schedule[-1]))
    max_scheduled_time_hour = max_scheduled_time.hour
    max_scheduled_time_date = max_scheduled_time
    max_scheduled_time_second = max_scheduled_time.second
    latest = times_to_schedule[-1]
    next_scheduled_time_hour = None
    next_scheduled_time_date = None
    if max_scheduled_time_hour == latest:
      next_scheduled_time_hour = times_to_schedule[0]
    else:
      index = times_to_schedule.index(max_scheduled_time_hour)
      next_index = index + 1
      next_scheduled_time_hour = times_to_schedule[next_index]
    if max_scheduled_time_hour == latest:
      next_scheduled_time_date = (Date(max_scheduled_time_date)+1)()
    else:
      next_scheduled_time_date = Date(max_scheduled_time_date)()
    next_scheduled_time = next_scheduled_time_date.replace(hour=next_scheduled_time_hour,second=max_scheduled_time_second)
    next_scheduled_time_timestamp = int(timestamp(next_scheduled_time))
    return next_scheduled_time_timestamp
  def get_next_scheduled_times(page,publish_times,start_date,count):
    all_data = []
    page = Get(Facebookpage,name=page)
    start_idx = 0
    for i in range(count):
      new = start_date.replace(hour=publish_times[start_idx])
      start_idx = start_idx + 1
      if start_idx+1 > len(publish_times):
        start_idx = 0
        start_date = start_date + timedelta(days=1)
      all_data.append(new)
    return all_data
  def get_pages():
    Shop()(All(Shop)[0].shop_abbreviation) # set the api
    user = get_user()
    pages = keycall("export_all_data", user.get_accounts(params={"limit":5000}))
    [tryprocess(Facebookpage(facebook_id=i["id"],name=i["name"],url="https://facebook.com/%s"%i["id"]).save,) for i in pages]
    [Update(Get(Facebookpage,facebook_id=i["id"]),token=i["access_token"]) for i in pages]
    [Update(Get(Facebookpage,facebook_id=i["id"]),publish_times = [14,19]) for i in pages]
    [Del(i) for i in All(Facebookpage) if i.name not in sud("name",pages)]
    return pages
  def get_post_reactions(page_name, post_id):
    page = Get(Facebookpage, name = page_name)
    url = "https://graph.facebook.com/%s/reactions"%(post_id)
    token = page.token
    params = {"access_token":token, "fields":["total_count"],"summary":"total_count"}
    r = requests.get(url, params = params)
    data = json.loads(r.text)
    total_count = data["summary"]["total_count"]
    return total_count
  def get_posted_posts(page_name):
    page = Get(Facebookpage, name = page_name)
    facebook_id = page.facebook_id
    url = "https://graph.facebook.com/%s/feed"%(facebook_id)
    token = page.token
    params = {"access_token":token, "fields":["created_time","message","id"], "limit":100}
    r = requests.get(url, params = params)
    all_data = []
    data = json.loads(r.text)["data"]
    all_data.extend(data)
    response = json.loads(r.text)
    while "next" in response.get("paging",[]):
      next_url = response["paging"]["next"]
      r = requests.get(next_url)
      response = json.loads(r.text)
      data = json.loads(r.text)["data"]
      all_data.extend(data)
    return all_data
  def get_promoted_object():
    promoted_object = {    "custom_event_type": "PURCHASE",     "pixel_id": str(Shop()(adset_to_create.shop_abbreviation).Facebook_Pixel_ID),    "pixel_rule": "{\"event\":{\"eq\":\"Purchase\"}}"    }
    return promoted_object
  def get_redirect_from_ad_copy(ad_copy):
    return re.findall(r"[:/a-zA-Z0-9]+\.[/a-zA-Z0-9-]+",body)
  def get_redirects(shop):
    redirects = sum([shop.shopify.Redirect.find(status="any", limit=250, page=i) for i in range(1,10)],[])
    return redirects
  def get_scheduled_posts(page_name):
    page = Get(Facebookpage, name = page_name)
    facebook_id = page.facebook_id
    url = "https://graph.facebook.com/%s/scheduled_posts"%(facebook_id)
    token = page.token
    params = {"access_token":token, "fields":["scheduled_publish_time"], "limit":100}
    r = requests.get(url, params = params)
    all_data = []
    data = json.loads(r.text)["data"]
    all_data.extend(data)
    response = json.loads(r.text)
    while "next" in response.get("paging",[]):
      next_url = response["paging"]["next"]
      r = requests.get(next_url)
      response = json.loads(r.text)
      data = json.loads(r.text)["data"]
      all_data.extend(data)
    [setitem(i,"scheduled_publish_time",timestamp(i["scheduled_publish_time"],False)) for i in all_data]
    return all_data
  def get_url_from_body(x):
    return getitem(re.findall(".*/.*",x),0,"None").split(" ")[-1]
  def get_user():
    a_shop()
    from facebookads.adobjects.user import User
    api = FacebookAdsApi.init(app_id=a_shop().Facebook_Business_App_ID,app_secret=a_shop().Facebook_Business_App_Secret,access_token=a_shop().Facebook_Business_App_Token)
    return User(fbid="me", api=api)
  def print_sorted_audiences():
    auds = Audience.objects.all()
    auds = keysort('pcs', auds, tcer=True)
    CSV().csvprint(auds, colnames=['pcs','roi','spent','pcv', 'name', 'niche', 'id'])
  def print_targeting_data(data):
    print("Targeting DATA for adset:\n\
            1. Age Min: %s\n\
            2. Age Max: %s\n\
            3. Gender: %s\n\
            4. Pixel Goals: %s\n\
            5. Attribution Spec: %s\n\
            6. Device Platforms: %s\n\
            7. Publisher Platforms: %s\n\
            8. Targeting Optimization: %s\n"%(data['targeting']['age_min'], data['targeting']['age_max'],
                                            data['targeting']['genders'], data['promoted_object']['custom_event_type'],
                                            data['attribution_spec'][0]['window_days'], data['targeting']['device_platforms'],
                                            data['targeting']['publisher_platforms'], data['targeting']['targeting_optimization']))
  def run():
    products_csv=os.path.expanduser('~/tavern/tavern/products.csv')
    data = CSV().DictRead(products_csv)
    shop = Shop()(All(Shop)[0].shop_abbreviation)

    # dicts = []
    for i in data:
      if i['added'] == "FAILED":
        products = productsFeed(shop)
        for j in products:
          if j.title == i['title']:
            j.delete()
      if i['added'] == 'FALSE':
        p = Aliexpress_Products().create_product(i['url'].split('?')[0], i['niche'], i['item_type'], i['title'], i['description'])
        input("Adjust Images, State / Add to Body - ")
        url = input("Input URL: ")
        p = shop.shopify.Product.find(id_=p.id)
        caption = create_caption(p, shop, i['caption'], url)
        advertise(url, p, caption)


    print("Added items \n\n")
  def t_format_ids(ids):
    return [{"interests": [{'id':i} for i in ids]}]
  def t_format_resp(resp):
    payload = []
    for i in resp:
      if i.get('valid',True) == True:
        payload.append({'id':i['id'], 'audience_size':i['audience_size'],'name':i['name'],
                        'category':i.get('disambiguation_category',''), 'topic':i.get('topic','')})
    return payload
  def t_reach_estimate(shop, ids=None):
    account = AdAccount('act_%s'%shop.Facebook_Business_Ad_Account_ID)
    t_spec = {'age_max': 65,
             'age_min': 18,
             'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
             'device_platforms': ['mobile', 'desktop'],
             'facebook_positions': ['feed', 'right_hand_column', 'instant_article'],
             'geo_locations': {'countries': ['US'], 'location_types': ['home']},
             'publisher_platforms': ['facebook', 'audience_network'],
             'targeting_optimization': 'none',
             'flexible_spec': []
             }
    # added this 2nd t_spec in as this is how based on 10/2018 targeting was by default
    t_spec = {'age_max': 65,
             'age_min': 18,
             #'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
             'device_platforms': ['mobile'],
             'facebook_positions': ['feed'],
             'geo_locations': {'countries': ['US'],},
             'publisher_platforms': ['facebook'],
             'targeting_optimization': 'none',
             'flexible_spec': []
             }
    if ids:
      t_spec['flexible_spec'] = t_format_ids(ids)
    params = {
        #'currency': 'USD',
        #'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
        'targeting_spec': t_spec, }
    reach_estimate = account.get_reach_estimate(params=params)
    return reach_estimate[0]["users"]
  def t_search(q,limit=10000):
    resp = TargetingSearch.search(params={'q':q,'type':'adinterest','limit':limit})
    return t_format_resp(resp)
  def t_suggestion(names):
    resp = TargetingSearch.search(params={'interest_list':list(names), 'type':'adinterestsuggestion', 'limit':10000})
    return t_format_resp(resp)
  def update_adset_names_from_body_url():
    a_shop()
    for adset in Adset.objects.filter(is_created=True):
      url = get_url_from_body(adset.body)
      if "bit.ly" in url:
        url = requests.get(url).url.replace("/products","")
      x = AdSet(adset.adset_id)
      x.remote_read(fields=["name", "daily_budget", "targeting"])

      #name = url
      #name = "%s , %s" % (x["daily_budget"], url)
      name = "US %s-%s"%(x["targeting"]["age_min"], x["targeting"]["age_max"])
      if x["name"] != name:
        ad = x.get_ads()[0]
        x.remote_update(params={"name":name})
        ad.remote_update(params={"name":name})
  def update_audience_data_specs():
    file = os.path.expanduser("~/Downloads/SPS_Deleted_Lifetime.csv")
    data = CSV().DictRead(file)
    for i in Audience.objects.all():
        pcs = 0
        for j in data:
            try:
              ad_data = eval(j['Ad Set Name'])
              if ad_data['audname'] == i.name:
                  pcs += int(j['Website Purchases'])
            except:pass
        i.pcs = pcs
        print(i.pcs)
        i.save()
  globals().update(locals())
class AdsetCreater:
  def __call__(self,fbid,url,caption,page_id,interest_ids=[]):
    try:
      """ ::: Make sure to Check If URL in CAPTION ie NO <redirect_url> &&, request200 url. ::: """
      try:get_url_from_body(caption)
      except Exception as e: redprint(e); return
      """ ::: request200 url ::: """

      #h = get_url_from_body(caption)
      """
      h = get_url_from_body( "".join(re.findall(r"[a-zA-Z0-9/:- .\n]",caption))  )
      while True:
        r = requests.get(h) if(h.startswith("http")) else (requests.get( ("https://"+h) ))
        t = r.url.split("/")[-1].split("?")[0]
        if(200!=r.status_code):
          redinput("(before Campaign Creation) \n 200!=status_code for %s\n\n\nASSOCIATED_CAPTION:\n%s\n\n" % (h,caption,"please fix the redirect or something, maybe it was erried"))
        elif(200==r.status_code):
          redprint("200==status_code for %s\n\n\nASSOCIATED_CAPTION:\n%s" % (h,caption))
          break
      """


      # url = "https://images.homedepot-static.com/productImages/1029e9c6-2eb6-4278-8a35-4b7e4d4737bb/svn/autumn-wood-lifeproof-porcelain-tile-lp32624hd1pr-64_1000.jpg"
      c = Campaign(parent_id="act_{}".format(fbid))
      c["name"] = "Conversions"
      c["buying_type"] = "AUCTION"
      c["objective"] = "CONVERSIONS"
      c.save()
      a = AdSet(parent_id="act_{}".format(fbid))
      #a["name"] = "US 18+"
      a["campaign_id"] = c["id"]
      a["daily_budget"] = 500
      a["name"] = "US 18+ "# + t
      a["optimization_goal"] = "OFFSITE_CONVERSIONS"
      a["promoted_object"] = {"custom_event_type": "PURCHASE", "pixel_id": Filter(Shop,Facebook_Business_Ad_Account_ID=fbid)[0].Facebook_Pixel_ID}
      a["start_time"] = "%s 6:00:00 EST"%(Date().dt(0) if datetime.now().hour in [0,1,2] else Date().dt(1))
      #@[2018.12.6 10:26 PM[mvdto(-1)]]a["start_time"] = "%s 5:00:00 EST"%(Date().dt(1) if datetime.now().hour in [0,1,2] else Date().dt(2))
      a["billing_event"] = "IMPRESSIONS"
      a["bid_strategy"] = "LOWEST_COST_WITHOUT_CAP"
      a["targeting"] = dict(age_min = 18,
                            device_platforms = ["mobile"],
                            facebook_positions = ["feed"],
                            publisher_platforms = ["facebook"],
                            targeting_optimization = "none",
                            geo_locations = {"countries": ["US"], "location_types": ["home", "recent"]},
                            flexible_spec = t_format_ids(interest_ids),
                            )
      a.save()
      v = Ad(parent_id="act_{}".format(fbid))
      #@[2018.12.8][Tried accessing nonexisting field (url_tags) on node type (Adgroup)]v["url_tags"] = "adset_id=%s"%(a["id"])
      v["name"] = "US 18+ "# + t
      v["adset_id"] = a["id"]
      (lambda fbid=fbid,url=url,caption=caption,page_id=page_id: [
      setitem(globals(),"image",AdImage(parent_id="act_{}".format(fbid)))  ,  
      #setitem(globals()["image"],"filename", Images().contrast_sharpen(Images().download_and_resize(url, 1200)))  ,  
      setitem(globals()["image"],"filename", Images().contrast_sharpen(Images().download_and_resize(url, 1200),contrast=True,sharpen=False))  ,  
      globals()["image"].remote_create()  ,  
      setitem(globals(),"photo_data",AdCreativePhotoData())  ,  
      setitem(globals()["photo_data"],"image_hash",globals()["image"]["hash"])  ,  
      setitem(globals()["photo_data"],"caption",caption)  ,  
      setitem(globals()["photo_data"],"page_welcome_message","Hello. Do you need any assistance?")  ,  
      setitem(globals(),"object_story_spec",AdCreativeObjectStorySpec())  ,  
      setitem(globals()["object_story_spec"],"page_id",page_id)  ,  
      setitem(globals()["object_story_spec"],"photo_data",globals()["photo_data"])  ,  
      setitem(globals(),"creative",AdCreative(parent_id="act_%s"%fbid))  ,  
      setitem(globals()["creative"],"name","Dark Post")  ,  
      setitem(globals()["creative"],"object_story_spec",globals()["object_story_spec"])  ,  
      "ajergcwonirgsncraoigncasdfkadpaksogranopgas;nrgoasingr"  ,  
      # globals()["creative"].remote_create()  ,  
      ])()
      v["creative"] = globals()["creative"]

      if ADSET_TESTING == True:
        a["status"] = "PAUSED"
        a.remote_update()

      v.save()
      return int(a["campaign_id"]), int(v["adset_id"])
    except Exception as e:
      redprint(e)
      redprint("deleting ")
      OSA.notify("deleting. ")
      OSA.notify(str(e))
      tryprocess(c.remote_delete); tryprocess(a.remote_delete); tryprocess(v.remote_delete)
class Adsetinsight_Algorithms:
  def one(self):
    """ ::: Get all adsethourlyinsights with sales. Then, keep adding impressions, get average hour/impression count of 1st sale. :::"""
    x = [keysort("date",Adsethourlyinsight.objects.filter(adset_id=i),tcer=False) for i in set(key("adset_id",Adsethourlyinsight.objects.all())) if list(set(key("website_purchase", Adsethourlyinsight.objects.filter(adset_id=i)))) != [0]]
    v = []
    for i in x:
      impressions = 0
      for idx,j in enumerate(i):
        impressions += j.impression
        if j.website_purchase != 0:
          v.append([impressions, idx])
          break
    print(  "hour       ", sum([b[1] for b in v])/len(v)  )
    print(  "impressions", sum([b[0] for b in v])/len(v)  )
  def one_data(self):
    """ ::: Get all adsethourlyinsights with sales. Then, keep adding impressions, get average hour/impression count of 1st sale. :::"""
    x = set(key("adset_id",Adsethourlyinsightdata.objects.all()))
    data = []
    for i in x:
      if list(set(key("website_purchase_move", Adsethourlyinsightdata.objects.filter(adset_id=i)))) != [0]:      
        data.append(keysort("date",Adsethourlyinsightdata.objects.filter(adset_id=i),tcer=False) )
    v = []
    for i in data:
      impression_moves = 0
      for idx,j in enumerate(i):
        impression_moves += j.impression_move
        if j.website_purchase_move != 0:
          v.append([impression_moves, idx])
          break
    print(  "hour       ", sum([b[1] for b in v])/len(v)  )
    print(  "impressions", sum([b[0] for b in v])/len(v)  )
  def two(self):
    for adset in Adset.objects.filter(is_created=True):
      if adset.status=="ACTIVE":
        data = keysort("date", Adsethourlyinsight.objects.filter(adset_id=adset.adset_id), tcer=False)
        impressions = 0; sales = 0
        for x in data:

          impressions+=x.impression
          sales+=x.website_purchase

          print(impressions, sales)
          if impressions > 500:
            if sales < 1:
              print("stop")
              print("[adset_id][%s]"%adset.adset_id)
              input("please check it, impressions: %s, sales: %s" % (impressions, sales))
              Adset(adset.adset_id).remote_update(params={"status":"PAUSED"})
class Interest_Tools(DecisionTree):
  def t_format_resp(self, resp):
    payload = []
    for i in resp:
      if i.get('valid',True) == True:
        payload.append({'id':i['id'], 'audience_size':i['audience_size'],'name':i['name'],
                        'category':i.get('disambiguation_category',''), 'topic':i.get('topic','')})
    return payload
  def t_search(self, q):
    resp = TargetingSearch.search(params={'q':q,'type':'adinterest','limit':10000})
    return self.t_format_resp(resp)
  def t_suggestion(self, names):
    resp = TargetingSearch.search(params={'interest_list':list(names), 'type':'adinterestsuggestion', 'limit':10000})
    return self.t_format_resp(resp)
  def t_format_ids(self, ids):
    return [{"interests": [{'id':i} for i in ids]}]
  def t_reach_estimate(self, shop, ids=None):
    account = AdAccount('act_%s'%shop.Facebook_Business_Ad_Account_ID)
    t_spec = {'age_max': 65,
             'age_min': 18,
             'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
             'device_platforms': ['mobile', 'desktop'],
             'facebook_positions': ['feed', 'right_hand_column', 'instant_article'],
             'geo_locations': {'countries': ['US'], 'location_types': ['home']},
             'publisher_platforms': ['facebook', 'audience_network'],
             'targeting_optimization': 'none',
             'flexible_spec': []
             }
    if ids:
      t_spec['flexible_spec'] = self.t_format_ids(ids)
    params = {
        'currency': 'USD',
        'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
        'targeting_spec': t_spec, }
    reach_estimate = account.get_reach_estimate(params=params)
    return reach_estimate[0]["users"]
class July_Adset_Utilities:
  def __init__(self):
    r""" This is important since looking at it now I forget the parameters and it looks as if i did not write any of it before"""
    #self.shop = shop
    # keep these for storage purposes
    a_shop()
    self.data_all_fields = ["spend","adset_id","date","frequency","impression","impression_cost","impression_rate","post_click","post_click_cost","post_click_rate","click","click_cost","click_rate","add_to_cart","add_to_cart_cost","add_to_cart_rate","website_purchase","website_purchase_cost","website_purchase_rate","spend","website_purchase_value","return_on_investment","reach","reach_cost","reach_rate","landing_page_view","landing_page_view_cost","landing_page_view_rate","fb_pixel_view_content","fb_pixel_view_content_cost","fb_pixel_view_content_rate","fb_pixel_initiate_checkout","fb_pixel_initiate_checkout_cost","fb_pixel_initiate_checkout_rate","page_engagement","page_engagement_cost","page_engagement_rate","post_engagement","post_engagement_cost","post_engagement_rate","post_reaction","post_reaction_cost","post_reaction_rate"]
    self.data_fields = ["spend","adset_id","date","frequency","impression","impression_cost","impression_rate","post_click","post_click_cost","post_click_rate","click","click_cost","click_rate","add_to_cart","add_to_cart_cost","add_to_cart_rate","website_purchase","website_purchase_cost","website_purchase_rate","spend","website_purchase_value","return_on_investment"]
    self.get_insight_fields = ["adset_id", "action_values", "actions", "adset_name", "clicks", "date_start", "date_stop", "frequency", "impressions", "reach", "relevance_score", "spend"]
    self.get_insight_params = {"time_increment": 1, "time_range": {"since": (Date()-0).datestr,"until": (Date()-0).datestr}}
  def get_campaigns(self, limit = 500):
    return self.shop.fb.get_campaigns(params = {"limit": limit})
  def get_adsets(self, campaign_id, limit = 500):
    scope_campaign = Campaign(campaign_id)
    adsets = scope_campaign.get_ad_sets(params = {"limit": limit})
    return adsets
  def pause_adset(self, adset_id):
    input("is this ok?: ")
    shop = Shop()( Adset.objects.get(adset_id=adset_id).shop_abbreviation)
    adset = AdSet(adset_id)
    adset["status"] = "PAUSED"
    status_check = adset.remote_update()
    print("adset %s: %s √"%(adset_id, status_check))
    assert status_check['status'] == 'PAUSED'
    Update(Get(Adset,adset_id=adset_id),status="PAUSED")
  def restart_adset(self, adset_id):
    input("is this ok?: ")
    shop = Shop()( Adset.objects.get(adset_id=adset_id).shop_abbreviation)
    adset = AdSet(adset_id)
    adset["status"] = "ACTIVE"
    status_check = adset.remote_update()
    print("adset %s: %s √"%(adset_id, status_check))
    assert status_check['status'] == 'ACTIVE'
    Update(Get(Adset,adset_id=adset_id),status="ACTIVE")
  def update_adset(self, id):
    new = Get(Adset,adset_id=id)
    data = AdSet(new.adset_id).remote_read(fields=["campaign_id","id"])
    new.campaign_id = data["campaign_id"]
    new.adset_id = data["id"]
    new.save()
  def update_adsetinsight_data(self, id, date_start = 5, date_end = 0, time_increment = 1, fields = ["adset_id", "action_values", "actions", "adset_name", "clicks", "date_start", "date_stop", "frequency", "impressions", "reach", "relevance_score", "spend"]):
    adset = Filter(Adset, adset_id=id)[0]
    self.shop = Shop()( adset.shop_abbreviation)
    data = [AttrDict(i.export_all_data()) for i in AdSet(adset.adset_id).get_insights(fields = fields, params={"time_increment": time_increment, "time_range": {"since": (Date()-date_start).datestr,"until": (Date()-date_end).datestr}})]
    for i in data:
      new = Adsetinsight()
      existing = Adsetinsight.objects.filter(adset_id = adset.adset_id, date = Date().myDatetimenow(Date(i.date_start).dateobj))
      if len(existing) == 1:
        new = existing[0]
        print("an existing")


      actions = i.get("actions", {})
      action_values = i.get("action_values", {})
      actions_dict = AttrDict(dict(zip(key("action_type", actions), key("value", actions))))
      action_values_dict = AttrDict(dict(zip(key("action_type", action_values), key("value", action_values))))

      spend = round(float(i.spend), 4)
      adset_id = adset.adset_id
      date = Date().myDatetimenow(Date(i.date_start).dateobj)
      frequency = round(float(i.frequency), 4)
      impression = int(i.impressions)
      if(0==impression):continue
      impression_cost = round(float(tryreturn(lambda: spend / impression)), 4)
      impression_rate = 0
      post_click = int(i.clicks)
      post_click_cost = round(float(tryreturn(lambda: spend / post_click)), 4)
      post_click_rate = round(float(tryreturn(lambda: post_click / impression)), 4)
      click = int(actions_dict.get("link_click", 0))
      click_cost = round(float(tryreturn(lambda: spend / click)), 4)
      click_rate = round(float(tryreturn(lambda: click / impression)), 4)
      add_to_cart = int(actions_dict.get("offsite_conversion.fb_pixel_add_to_cart", 0))
      add_to_cart_cost = round(float(tryreturn(lambda: spend / add_to_cart)), 4)
      try:add_to_cart_rate = round(float(tryreturn(lambda: add_to_cart / impression)), 4)
      except:add_to_cart_rate = 0 #(?)
      website_purchase = int(actions_dict.get("offsite_conversion.fb_pixel_purchase", 0))
      ##conversion_pixel_purchase = int(actions_dict.get("offsite_conversion", 0))
      ##if website_purchase > 0 and conversion_pixel_purchase == 0:
      ##  website_purchase = website_purchase
      ##if website_purchase > 0 and conversion_pixel_purchase > 0:
      ##  website_purchase = ((website_purchase+conversion_pixel_purchase) / 2)
      ##if website_purchase == 0 and conversion_pixel_purchase > 0:
      ##  website_purchase = conversion_pixel_purchase

      website_purchase_cost = round(float(tryreturn(lambda: spend / website_purchase)), 4)
      website_purchase_rate = round(float(tryreturn(lambda: website_purchase / impression)), 4)
      spend = round(float(i.spend), 4)
      website_purchase_value = round(float(action_values_dict.get("offsite_conversion.fb_pixel_purchase", 0)), 4)
      return_on_investment = round(float(tryreturn(lambda: website_purchase_value / spend)), 4)
      reach = int(i.reach)
      reach_cost = round(float(tryreturn(lambda: spend / reach)), 4)
      reach_rate = 0
      landing_page_view = int(actions_dict.get("landing_page_view", 0))
      landing_page_view_cost = round(float(tryreturn(lambda: spend / landing_page_view)), 4)
      landing_page_view_rate = round(float(tryreturn(lambda: landing_page_view / impression)), 4)
      fb_pixel_view_content = int(actions_dict.get("offsite_conversion.fb_pixel_view_content", 0))
      fb_pixel_view_content_cost = round(float(tryreturn(lambda: spend / fb_pixel_view_content)), 4)
      fb_pixel_view_content_rate = round(float(fb_pixel_view_content / impression), 4)
      fb_pixel_initiate_checkout = int(actions_dict.get("offsite_conversion.fb_pixel_initiate_checkout", 0))
      fb_pixel_initiate_checkout_cost = round(float(tryreturn(lambda: spend / fb_pixel_initiate_checkout)), 4)
      fb_pixel_initiate_checkout_rate = round(float(fb_pixel_initiate_checkout / impression), 4)
      page_engagement = int(actions_dict.get("page_engagement", 0))
      page_engagement_cost = round(float(tryreturn(lambda: spend / page_engagement)), 4)
      page_engagement_rate = round(float(page_engagement / impression), 4)
      post_engagement = int(actions_dict.get("post_engagement", 0))
      post_engagement_cost = round(float(tryreturn(lambda: spend / post_engagement)), 4)
      post_engagement_rate = round(float(post_engagement / impression), 4)
      post_reaction = int(actions_dict.get("post_reaction", 0))
      post_reaction_cost = round(float(tryreturn(lambda: spend / post_reaction)), 4)
      post_reaction_rate = round(float(post_reaction / impression), 4)


      greenprint("[update_adsetinsight_data][spend][%s]"% spend)
      greenprint("[update_adsetinsight_data][adset_id][%s]"% adset_id)
      greenprint("[update_adsetinsight_data][date][%s]"% date)
      greenprint("[update_adsetinsight_data][frequency][%s]"% frequency)
      greenprint("[update_adsetinsight_data][impression][%s]"% impression)
      greenprint("[update_adsetinsight_data][impression_cost][%s]"% impression_cost)
      greenprint("[update_adsetinsight_data][impression_rate][%s]"% impression_rate)
      greenprint("[update_adsetinsight_data][post_click][%s]"% post_click)
      greenprint("[update_adsetinsight_data][post_click_cost][%s]"% post_click_cost)
      greenprint("[update_adsetinsight_data][post_click_rate][%s]"% post_click_rate)
      greenprint("[update_adsetinsight_data][click][%s]"% click)
      greenprint("[update_adsetinsight_data][click_cost][%s]"% click_cost)
      greenprint("[update_adsetinsight_data][click_rate][%s]"% click_rate)
      greenprint("[update_adsetinsight_data][add_to_cart][%s]"% add_to_cart)
      greenprint("[update_adsetinsight_data][add_to_cart_cost][%s]"% add_to_cart_cost)
      greenprint("[update_adsetinsight_data][add_to_cart_rate][%s]"% add_to_cart_rate)
      greenprint("[update_adsetinsight_data][website_purchase][%s]"% website_purchase)
      greenprint("[update_adsetinsight_data][website_purchase_cost][%s]"% website_purchase_cost)
      greenprint("[update_adsetinsight_data][website_purchase_rate][%s]"% website_purchase_rate)
      greenprint("[update_adsetinsight_data][spend][%s]"% spend)
      greenprint("[update_adsetinsight_data][website_purchase][%s]"% website_purchase_value)
      greenprint("[update_adsetinsight_data][offsite_conversion][%s]"% website_purchase_value)
      greenprint("[update_adsetinsight_data][website_purchase_value][%s]"% website_purchase_value)
      greenprint("[update_adsetinsight_data][return_on_investment][%s]"% return_on_investment)
      greenprint("[update_adsetinsight_data][reach][%s]"% reach)
      greenprint("[update_adsetinsight_data][reach_cost][%s]"% reach_cost)
      greenprint("[update_adsetinsight_data][reach_rate][%s]"% reach_rate)
      greenprint("[update_adsetinsight_data][landing_page_view][%s]"% landing_page_view)
      greenprint("[update_adsetinsight_data][landing_page_view_cost][%s]"% landing_page_view_cost)
      greenprint("[update_adsetinsight_data][landing_page_view_rate][%s]"% landing_page_view_rate)
      greenprint("[update_adsetinsight_data][fb_pixel_view_content][%s]"% fb_pixel_view_content)
      greenprint("[update_adsetinsight_data][fb_pixel_view_content_cost][%s]"% fb_pixel_view_content_cost)
      greenprint("[update_adsetinsight_data][fb_pixel_view_content_rate][%s]"% fb_pixel_view_content_rate)
      greenprint("[update_adsetinsight_data][fb_pixel_initiate_checkout][%s]"% fb_pixel_initiate_checkout)
      greenprint("[update_adsetinsight_data][fb_pixel_initiate_checkout_cost][%s]"% fb_pixel_initiate_checkout_cost)
      greenprint("[update_adsetinsight_data][fb_pixel_initiate_checkout_rate][%s]"% fb_pixel_initiate_checkout_rate)
      greenprint("[update_adsetinsight_data][page_engagement][%s]"% page_engagement)
      greenprint("[update_adsetinsight_data][page_engagement_cost][%s]"% page_engagement_cost)
      greenprint("[update_adsetinsight_data][page_engagement_rate][%s]"% page_engagement_rate)
      greenprint("[update_adsetinsight_data][post_engagement][%s]"% post_engagement)
      greenprint("[update_adsetinsight_data][post_engagement_cost][%s]"% post_engagement_cost)
      greenprint("[update_adsetinsight_data][post_engagement_rate][%s]"% post_engagement_rate)
      greenprint("[update_adsetinsight_data][post_reaction][%s]"% post_reaction)
      greenprint("[update_adsetinsight_data][post_reaction_cost][%s]"% post_reaction_cost)
      greenprint("[update_adsetinsight_data][post_reaction_rate][%s]"% post_reaction_rate)


      new.spend = spend
      new.ad_account_id = self.shop.Facebook_Business_Ad_Account_ID
      new.adset_id = adset_id
      new.date = date
      new.frequency = frequency
      new.impression = impression
      new.impression_cost = impression_cost
      new.impression_rate = impression_rate
      new.post_click = post_click
      new.post_click_cost = post_click_cost
      new.post_click_rate = post_click_rate
      new.click = click
      new.click_cost = click_cost
      new.click_rate = click_rate
      new.add_to_cart = add_to_cart
      new.add_to_cart_cost = add_to_cart_cost
      new.add_to_cart_rate = add_to_cart_rate
      new.website_purchase = website_purchase
      new.website_purchase_cost = website_purchase_cost
      new.website_purchase_rate = website_purchase_rate
      new.spend = spend
      new.website_purchase_value = website_purchase_value
      new.return_on_investment = return_on_investment
      new.reach = reach
      new.reach_cost = reach_cost
      new.reach_rate = reach_rate
      new.landing_page_view = landing_page_view
      new.landing_page_view_cost = landing_page_view_cost
      new.landing_page_view_rate = landing_page_view_rate
      new.fb_pixel_view_content = fb_pixel_view_content
      new.fb_pixel_view_content_cost = fb_pixel_view_content_cost
      new.fb_pixel_view_content_rate = fb_pixel_view_content_rate
      new.fb_pixel_initiate_checkout = fb_pixel_initiate_checkout
      new.fb_pixel_initiate_checkout_cost = fb_pixel_initiate_checkout_cost
      new.fb_pixel_initiate_checkout_rate = fb_pixel_initiate_checkout_rate
      new.page_engagement = page_engagement
      new.page_engagement_cost = page_engagement_cost
      new.page_engagement_rate = page_engagement_rate
      new.post_engagement = post_engagement
      new.post_engagement_cost = post_engagement_cost
      new.post_engagement_rate = post_engagement_rate
      new.post_reaction = post_reaction
      new.post_reaction_cost = post_reaction_cost
      new.post_reaction_rate = post_reaction_rate


      new.save()
  # https://developers.facebook.com/docs/marketing-api/click-tags
  def update_adsethourlyinsight_data(self, id, date_start = 5, date_end = 0, time_increment = 1, breakdowns=["hourly_stats_aggregated_by_advertiser_time_zone"], fields = ["adset_id", "action_values", "actions", "adset_name", "clicks", "date_start", "date_stop", "frequency", "impressions", "reach", "relevance_score", "spend"]):
    """
    date_start = 800
    date_end = 0
    time_increment = 1
    breakdowns=["hourly_stats_aggregated_by_advertiser_time_zone"]
    fields = ["adset_id", "action_values", "actions", "adset_name", "clicks", "date_start", "date_stop", "frequency", "impressions", "reach", "relevance_score", "spend"]
    insights = adset.get_insights(fields = fields, params={"time_increment": time_increment, "time_range": {"since": (Date()-date_start).datestr,"until": (Date()-date_end).datestr}}       )
    """
    # used to be date_start = 0 and date_end = 0, it only gets data for `today` but it could end early, ie, @/3hrs, date_start= 1 would have been better
    # 
    # In [25]: key("impression_cost",Adsethourlyinsight.objects.filter(adset_id=6110536376017))
    # Out[25]: [0.0259, 0.0355]
    adset = Filter(Adset,adset_id=id)[0]
    self.shop = Shop()( adset.shop_abbreviation)
    data = [AttrDict(i.export_all_data()) for i in AdSet(adset.adset_id).get_insights(fields = fields, params={"breakdowns": breakdowns, "time_increment": time_increment, "time_range": {"since": (Date()-date_start).datestr,"until": (Date()-date_end).datestr}})]

    for i in data:
      new = Adsethourlyinsight()
      date = (round((int(i.hourly_stats_aggregated_by_advertiser_time_zone.split(" - ")[0].split(":")[0])/24),2)+Date().myDatetimenow(Date(i.date_start).dateobj)  )
      distinct_print("[%s][%s]"%(date,i.hourly_stats_aggregated_by_advertiser_time_zone))
      for d in range(24):
        tryprocess(Adsethourlyinsight(ad_account_id=self.shop.Facebook_Business_Ad_Account_ID, date=(Date().myDatetimenow(Date(i.date_start).dateobj)+round((d/24),2)), adset_id=i.adset_id ).save)
      existing = Adsethourlyinsight.objects.filter(adset_id = adset.adset_id, date = date)
      if len(existing) == 1:
        new = existing[0]
        print("an existing")


      actions = i.get("actions", {})
      action_values = i.get("action_values", {})
      actions_dict = AttrDict(dict(zip(key("action_type", actions), key("value", actions))))
      action_values_dict = AttrDict(dict(zip(key("action_type", action_values), key("value", action_values))))

      spend = round(float(i.spend), 4)
      adset_id = adset.adset_id
      #date = Date().myDatetimenow(Date(i.date_start).dateobj)
      #frequency = round(float(i.frequency), 4)
      impression = int(i.impressions)
      if(0==impression):continue
      impression_cost = round(float(tryreturn(lambda: spend / impression)), 4)
      impression_rate = 0
      post_click = int(i.clicks)
      post_click_cost = round(float(tryreturn(lambda: spend / post_click)), 4)
      post_click_rate = round(float(tryreturn(lambda: post_click / impression)), 4)
      click = int(actions_dict.get("link_click", 0))
      click_cost = round(float(tryreturn(lambda: spend / click)), 4)
      click_rate = round(float(tryreturn(lambda: click / impression)), 4)
      add_to_cart = int(actions_dict.get("offsite_conversion.fb_pixel_add_to_cart", 0))
      add_to_cart_cost = round(float(tryreturn(lambda: spend / add_to_cart)), 4)
      try:add_to_cart_rate = round(float(tryreturn(lambda: add_to_cart / impression)), 4)
      except:add_to_cart_rate = 0 #(?)
      website_purchase = int(actions_dict.get("offsite_conversion.fb_pixel_purchase", 0))
      #conversion_pixel_purchase = int(actions_dict.get("offsite_conversion", 0))
      #if website_purchase > 0 and conversion_pixel_purchase == 0:
      #  website_purchase = website_purchase
      #if website_purchase > 0 and conversion_pixel_purchase > 0:
      #  website_purchase = ((website_purchase+conversion_pixel_purchase) / 2)
      #if website_purchase == 0 and conversion_pixel_purchase > 0:
      #  website_purchase = conversion_pixel_purchase
      website_purchase_cost = round(float(tryreturn(lambda: spend / website_purchase)), 4)
      website_purchase_rate = round(float(tryreturn(lambda: website_purchase / impression)), 4)
      spend = round(float(i.spend), 4)
      website_purchase_value = round(float(action_values_dict.get("offsite_conversion.fb_pixel_purchase", 0)), 4)
      return_on_investment = round(float(tryreturn(lambda: website_purchase_value / spend)), 4)
      #reach = int(i.reach)
      #reach_cost = round(float(tryreturn(lambda: spend / reach)), 4)
      #reach_rate = 0
      landing_page_view = int(actions_dict.get("landing_page_view", 0))
      landing_page_view_cost = round(float(tryreturn(lambda: spend / landing_page_view)), 4)
      landing_page_view_rate = round(float(tryreturn(lambda: landing_page_view / impression)), 4)
      fb_pixel_view_content = int(actions_dict.get("offsite_conversion.fb_pixel_view_content", 0))
      fb_pixel_view_content_cost = round(float(tryreturn(lambda: spend / fb_pixel_view_content)), 4)
      fb_pixel_view_content_rate = round(float(fb_pixel_view_content / impression), 4)
      fb_pixel_initiate_checkout = int(actions_dict.get("offsite_conversion.fb_pixel_initiate_checkout", 0))
      fb_pixel_initiate_checkout_cost = round(float(tryreturn(lambda: spend / fb_pixel_initiate_checkout)), 4)
      fb_pixel_initiate_checkout_rate = round(float(fb_pixel_initiate_checkout / impression), 4)
      page_engagement = int(actions_dict.get("page_engagement", 0))
      page_engagement_cost = round(float(tryreturn(lambda: spend / page_engagement)), 4)
      page_engagement_rate = round(float(page_engagement / impression), 4)
      post_engagement = int(actions_dict.get("post_engagement", 0))
      post_engagement_cost = round(float(tryreturn(lambda: spend / post_engagement)), 4)
      post_engagement_rate = round(float(post_engagement / impression), 4)
      post_reaction = int(actions_dict.get("post_reaction", 0))
      post_reaction_cost = round(float(tryreturn(lambda: spend / post_reaction)), 4)
      post_reaction_rate = round(float(post_reaction / impression), 4)



      new.spend = spend
      new.ad_account_id = self.shop.Facebook_Business_Ad_Account_ID
      new.adset_id = adset_id
      new.date = date
      #new.frequency = frequency
      new.impression = impression
      new.impression_cost = impression_cost
      new.impression_rate = impression_rate
      new.post_click = post_click
      new.post_click_cost = post_click_cost
      new.post_click_rate = post_click_rate
      new.click = click
      new.click_cost = click_cost
      new.click_rate = click_rate
      new.add_to_cart = add_to_cart
      new.add_to_cart_cost = add_to_cart_cost
      new.add_to_cart_rate = add_to_cart_rate
      new.website_purchase = website_purchase
      new.website_purchase_cost = website_purchase_cost
      new.website_purchase_rate = website_purchase_rate
      new.spend = spend
      new.website_purchase_value = website_purchase_value
      new.return_on_investment = return_on_investment
      #new.reach = reach
      #new.reach_cost = reach_cost
      #new.reach_rate = reach_rate
      new.landing_page_view = landing_page_view
      new.landing_page_view_cost = landing_page_view_cost
      new.landing_page_view_rate = landing_page_view_rate
      new.fb_pixel_view_content = fb_pixel_view_content
      new.fb_pixel_view_content_cost = fb_pixel_view_content_cost
      new.fb_pixel_view_content_rate = fb_pixel_view_content_rate
      new.fb_pixel_initiate_checkout = fb_pixel_initiate_checkout
      new.fb_pixel_initiate_checkout_cost = fb_pixel_initiate_checkout_cost
      new.fb_pixel_initiate_checkout_rate = fb_pixel_initiate_checkout_rate
      new.page_engagement = page_engagement
      new.page_engagement_cost = page_engagement_cost
      new.page_engagement_rate = page_engagement_rate
      new.post_engagement = post_engagement
      new.post_engagement_cost = post_engagement_cost
      new.post_engagement_rate = post_engagement_rate
      new.post_reaction = post_reaction
      new.post_reaction_cost = post_reaction_cost
      new.post_reaction_rate = post_reaction_rate


      #new.save()
      new.save()
  def update_adsetinsight_data_find_which_adset_had_the_order(self, date_start = 0, date_end = 0, time_increment = 1, fields = ["adset_id", "action_values", "actions", "adset_name", "clicks", "date_start", "date_stop", "frequency", "impressions", "reach", "relevance_score", "spend"], is_a_shopify_order_match_check=False, is_a_shopify_order_match_check_orders=[]):
    redprint("Running 'update_adsetinsight_data_find_which_adset_had_the_order' ... ")
    for adset in Adset.objects.filter(is_created=True):
      self.shop = Shop()( adset.shop_abbreviation)
      data = [AttrDict(i.export_all_data()) for i in AdSet(adset.adset_id).get_insights(fields = fields, params={"time_increment": time_increment, "time_range": {"since": (Date()-date_start).datestr,"until": (Date()-date_end).datestr}})]
      adset_shopify_order_matches = []
      for i in data:
        new = Adsetinsight()
        existing = Adsetinsight.objects.filter(adset_id = adset.adset_id, date = Date().myDatetimenow(Date(i.date_start).dateobj))
        if len(existing) == 1:
          new = existing[0]
          print("an existing")


        actions = i.get("actions", {})
        action_values = i.get("action_values", {})
        actions_dict = AttrDict(dict(zip(key("action_type", actions), key("value", actions))))
        action_values_dict = AttrDict(dict(zip(key("action_type", action_values), key("value", action_values))))

        spend = round(float(i.spend), 4)
        adset_id = adset.adset_id
        date = Date().myDatetimenow(Date(i.date_start).dateobj)
        frequency = round(float(i.frequency), 4)
        impression = int(i.impressions)
        if(0==impression):continue
        impression_cost = round(float(tryreturn(lambda: spend / impression)), 4)
        impression_rate = 0
        post_click = int(i.clicks)
        post_click_cost = round(float(tryreturn(lambda: spend / post_click)), 4)
        post_click_rate = round(float(tryreturn(lambda: post_click / impression)), 4)
        click = int(actions_dict.get("link_click", 0))
        click_cost = round(float(tryreturn(lambda: spend / click)), 4)
        click_rate = round(float(tryreturn(lambda: click / impression)), 4)
        add_to_cart = int(actions_dict.get("offsite_conversion.fb_pixel_add_to_cart", 0))
        add_to_cart_cost = round(float(tryreturn(lambda: spend / add_to_cart)), 4)
        try:add_to_cart_rate = round(float(tryreturn(lambda: add_to_cart / impression)), 4)
        except:add_to_cart_rate = 0 #(?)
        website_purchase = int(actions_dict.get("offsite_conversion.fb_pixel_purchase", 0))
        #conversion_pixel_purchase = int(actions_dict.get("offsite_conversion", 0))
        #if website_purchase > 0 and conversion_pixel_purchase == 0:
        #  website_purchase = website_purchase
        #if website_purchase > 0 and conversion_pixel_purchase > 0:
        #  website_purchase = ((website_purchase+conversion_pixel_purchase) / 2)
        #if website_purchase == 0 and conversion_pixel_purchase > 0:
        #  website_purchase = conversion_pixel_purchase
        website_purchase_cost = round(float(tryreturn(lambda: spend / website_purchase)), 4)
        website_purchase_rate = round(float(tryreturn(lambda: website_purchase / impression)), 4)
        spend = round(float(i.spend), 4)
        website_purchase_value = round(float(action_values_dict.get("offsite_conversion.fb_pixel_purchase", 0)), 4)
        return_on_investment = round(float(tryreturn(lambda: website_purchase_value / spend)), 4)
        reach = int(i.reach)
        reach_cost = round(float(tryreturn(lambda: spend / reach)), 4)
        reach_rate = 0
        landing_page_view = int(actions_dict.get("landing_page_view", 0))
        landing_page_view_cost = round(float(tryreturn(lambda: spend / landing_page_view)), 4)
        landing_page_view_rate = round(float(tryreturn(lambda: landing_page_view / impression)), 4)
        fb_pixel_view_content = int(actions_dict.get("offsite_conversion.fb_pixel_view_content", 0))
        fb_pixel_view_content_cost = round(float(tryreturn(lambda: spend / fb_pixel_view_content)), 4)
        fb_pixel_view_content_rate = round(float(fb_pixel_view_content / impression), 4)
        fb_pixel_initiate_checkout = int(actions_dict.get("offsite_conversion.fb_pixel_initiate_checkout", 0))
        fb_pixel_initiate_checkout_cost = round(float(tryreturn(lambda: spend / fb_pixel_initiate_checkout)), 4)
        fb_pixel_initiate_checkout_rate = round(float(fb_pixel_initiate_checkout / impression), 4)
        page_engagement = int(actions_dict.get("page_engagement", 0))
        page_engagement_cost = round(float(tryreturn(lambda: spend / page_engagement)), 4)
        page_engagement_rate = round(float(page_engagement / impression), 4)
        post_engagement = int(actions_dict.get("post_engagement", 0))
        post_engagement_cost = round(float(tryreturn(lambda: spend / post_engagement)), 4)
        post_engagement_rate = round(float(post_engagement / impression), 4)
        post_reaction = int(actions_dict.get("post_reaction", 0))
        post_reaction_cost = round(float(tryreturn(lambda: spend / post_reaction)), 4)
        post_reaction_rate = round(float(post_reaction / impression), 4)

        if is_a_shopify_order_match_check == True:
          if len(existing) == 1:
            if existing[0].website_purchase > website_purchase:
              print("Found a new conversion for this Ad Set. Adding it to ")
              adset_shopify_order_matches.append(existing[0])
        print("\n")
        redprint("adset-shopify-order-matches: %s | is_a_shopify_order_match_check_orders (count of shopify orders): %s" % (len(adset_shopify_order_matches), len(is_a_shopify_order_match_check_orders)) )
        print("\n")
        """ since this is so bad: the factors are   [count_new_purchases, count_new_orders, count_new_adsets, matching_by_order_difference, and how badly this matters,--  of course you can assume 1 order at most per minute]"""
        # run analysis here, -2 indents b/c the assumption is for i in data(of adset) iterates through 1 adset | keep it here, which will be fine for the next since you are saving the variables: order AND adset
        if   (is_a_shopify_order_match_check==True)   and   (len(adset_shopify_order_matches)==1)   and   (len(is_a_shopify_order_match_check_orders)==1)  :
          adset_shopify_order_match = adset_shopify_order_matches[0]
          adset_shopify_order_match.order_ids.append(is_a_shopify_order_match_check_orders[0].id)
          adset_shopify_order_match.save()
        #elif (is_a_shopify_order_match_check==True)   and   (len(adset_shopify_order_matches)!=len(is_a_shopify_order_match_check_orders))  :
        #  """ This will occur if  for example: is_a_shopify_order_match_check_orders > 1, say 2.     if 2 is unequal to count of   adset_shopify_order_matches,;;˚ then you got 2 sales in shopify confirmed, and less than 1/0 adsets   had new orders.                """
        #  """Assuming a 0-10 second Pixel-Update timeframe--   you will want to solve the case of if 0 adset_shopify_order_matches exist, which is simply assuming `should-have-posted` and assuming `nothing-new-purchasesed` """
        #  """ then is the case of a different sort of match: [where you have to choose which order_id of the 2 orders to update to the adset  ]   \route 1: exacting the closer order_created_time(seconds) to the adset_update_time   \route 2: exacting the closer order amount/2 to the adset.  \ """
        #  """ so route 1: can i find the purchase time to the minute or second ( i dont know)"""
        #  for adset in adset_shopify_order_matches:
        #    price_differences = []
        #    for shopify_order in is_a_shopify_order_match_check_orders:
        #      adset_value_increase = website_purchase_value - existing[0].website_purchase_value
        #      price_difference  = adset_value_increase - total_price
        #      price_differences.append([shopify_order, price_difference])
        #    smallest_difference = min(price_differences)
        #    for price_difference in price_differences:
        #      if price_difference[1] == smallest_difference:
        #        print("price_difference of %s == smallest_difference: %s"% (price_difference[1], smallest_difference))
        #        shopify_order = price_difference[0]
        #        adset.order_ids = [] if adset.order_ids == None else adset.order_ids
        #        adset.order_ids.append(shopify.order_id)
        #        print("adset of id: %s which has previous conversion value of %s and now current conversion value of %s now is matched with order id: %s of total amount %s" % (existing[0].adset_id, existing[0].website_purchase_value, website_purchase_value, shopify_order.id, shopify_order.total_amount))
        #elif (is_a_shopify_order_match_check==True)   and   (len(adset_shopify_order_matches)!=len(is_a_shopify_order_match_check_orders))  :
        #  # try to match by price as well. assuming 2 new orders, 2 new adsets with orders.        if the case 2 new orders 1 new adset with orders, then due to the price match -- that 1 new adset will 
        #  for adset in adset_shopify_order_matches:
        #    price_differences = []
        #    for shopify_order in is_a_shopify_order_match_check_orders:
        #      adset_value_increase = website_purchase_value - existing[0].website_purchase_value
        #      price_difference  = adset_value_increase - total_price
        #      price_differences.append([shopify_order, price_difference])
        #    smallest_difference = min(price_differences)
        #    for price_difference in price_differences:
        #      if price_difference[1] == smallest_difference:
        #        print("price_difference of %s == smallest_difference: %s"% (price_difference[1], smallest_difference))
        #        shopify_order = price_difference[0]
        #        adset.order_ids = [] if adset.order_ids == None else adset.order_ids
        #        adset.order_ids.append(shopify.order_id)
        #        print("adset of id: %s which has previous conversion value of %s and now current conversion value of %s now is matched with order id: %s of total amount %s" % (existing[0].adset_id, existing[0].website_purchase_value, website_purchase_value, shopify_order.id, shopify_order.total_amount))


        print("spend: %s"% spend)
        print("adset_id: %s"% adset_id)
        print("date: %s"% date)
        print("frequency: %s"% frequency)
        print("impression: %s"% impression)
        print("impression_cost: %s"% impression_cost)
        print("impression_rate: %s"% impression_rate)
        print("post_click: %s"% post_click)
        print("post_click_cost: %s"% post_click_cost)
        print("post_click_rate: %s"% post_click_rate)
        print("click: %s"% click)
        print("click_cost: %s"% click_cost)
        print("click_rate: %s"% click_rate)
        print("add_to_cart: %s"% add_to_cart)
        print("add_to_cart_cost: %s"% add_to_cart_cost)
        print("add_to_cart_rate: %s"% add_to_cart_rate)
        print("website_purchase: %s"% website_purchase)
        print("website_purchase_cost: %s"% website_purchase_cost)
        print("website_purchase_rate: %s"% website_purchase_rate)
        print("spend: %s"% spend)
        print("website_purchase_value: %s"% website_purchase_value)
        print("return_on_investment: %s"% return_on_investment)
        print("reach: %s"% reach)
        print("reach_cost: %s"% reach_cost)
        print("reach_rate: %s"% reach_rate)
        print("landing_page_view: %s"% landing_page_view)
        print("landing_page_view_cost: %s"% landing_page_view_cost)
        print("landing_page_view_rate: %s"% landing_page_view_rate)
        print("fb_pixel_view_content: %s"% fb_pixel_view_content)
        print("fb_pixel_view_content_cost: %s"% fb_pixel_view_content_cost)
        print("fb_pixel_view_content_rate: %s"% fb_pixel_view_content_rate)
        print("fb_pixel_initiate_checkout: %s"% fb_pixel_initiate_checkout)
        print("fb_pixel_initiate_checkout_cost: %s"% fb_pixel_initiate_checkout_cost)
        print("fb_pixel_initiate_checkout_rate: %s"% fb_pixel_initiate_checkout_rate)
        print("page_engagement: %s"% page_engagement)
        print("page_engagement_cost: %s"% page_engagement_cost)
        print("page_engagement_rate: %s"% page_engagement_rate)
        print("post_engagement: %s"% post_engagement)
        print("post_engagement_cost: %s"% post_engagement_cost)
        print("post_engagement_rate: %s"% post_engagement_rate)
        print("post_reaction: %s"% post_reaction)
        print("post_reaction_cost: %s"% post_reaction_cost)
        print("post_reaction_rate: %s"% post_reaction_rate)


        new.spend = spend
        new.ad_account_id = self.shop.Facebook_Business_Ad_Account_ID
        new.adset_id = adset_id
        new.date = date
        new.frequency = frequency
        new.impression = impression
        new.impression_cost = impression_cost
        new.impression_rate = impression_rate
        new.post_click = post_click
        new.post_click_cost = post_click_cost
        new.post_click_rate = post_click_rate
        new.click = click
        new.click_cost = click_cost
        new.click_rate = click_rate
        new.add_to_cart = add_to_cart
        new.add_to_cart_cost = add_to_cart_cost
        new.add_to_cart_rate = add_to_cart_rate
        new.website_purchase = website_purchase
        new.website_purchase_cost = website_purchase_cost
        new.website_purchase_rate = website_purchase_rate
        new.spend = spend
        new.website_purchase_value = website_purchase_value
        new.return_on_investment = return_on_investment
        new.reach = reach
        new.reach_cost = reach_cost
        new.reach_rate = reach_rate
        new.landing_page_view = landing_page_view
        new.landing_page_view_cost = landing_page_view_cost
        new.landing_page_view_rate = landing_page_view_rate
        new.fb_pixel_view_content = fb_pixel_view_content
        new.fb_pixel_view_content_cost = fb_pixel_view_content_cost
        new.fb_pixel_view_content_rate = fb_pixel_view_content_rate
        new.fb_pixel_initiate_checkout = fb_pixel_initiate_checkout
        new.fb_pixel_initiate_checkout_cost = fb_pixel_initiate_checkout_cost
        new.fb_pixel_initiate_checkout_rate = fb_pixel_initiate_checkout_rate
        new.page_engagement = page_engagement
        new.page_engagement_cost = page_engagement_cost
        new.page_engagement_rate = page_engagement_rate
        new.post_engagement = post_engagement
        new.post_engagement_cost = post_engagement_cost
        new.post_engagement_rate = post_engagement_rate
        new.post_reaction = post_reaction
        new.post_reaction_cost = post_reaction_cost
        new.post_reaction_rate = post_reaction_rate


        #new.save()
        new.save()
  # 2. Stop AdSets based on today- data
  def stop_adset_based_on_today_data(self, id):

    todays_date = int(Date().myDatetimenow())
    # check it out. i filtered adset insights to those which will have the id.
    adsetinsights = Adsetinsight.objects.filter(date=todays_date, adset_id=id)
    #cyanprint("[Count active today][%s]"%len(adsetinsights))
    for adsetinsight in adsetinsights:
      if Adset.objects.get(adset_id=adsetinsight.adset_id).status == "ACTIVE":
        if (adsetinsight.spend >= 20 and adsetinsight.website_purchase == 0):#   or   (adsetinsight.impression_cost > .015 and adsetinsight.website_purchase == 0):
          redprint("[stop_adsets_based_on_today_data][%s][%s][%s] [%s]['!=OK']"%(adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
          July_Adset_Utilities().pause_adset(adset_id=adsetinsight.adset_id)
        else:
          greenprint("[%s][%s][%s] [%s]['OK']"%(adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
  # 1. Stop AdSets based on summation data
  def stop_adset_based_on_past_data(self, id):
    # maybe i should print out in sentences?  as when i read the data fields, i'm having to utter words in my head to transmit the data through my brain
    todays_date = int(Date().myDatetimenow())
    # check it out, i filtered adset insights to those containing this id as the adset_id
    adsetinsights = Adsetinsight.objects.filter(date=todays_date, adset_id=id)
    print("[Count active today][%s]"%len(adsetinsights))
    """ this will be a unique iteration for adsetinsights with date(delivery) today AND with adset_id """  
    adset_ids_unique = list(sorted(list(set(key("adset_id", adsetinsights)))))
    for adset_id in adset_ids_unique:
      adsetinsights = Adsetinsight.objects.filter(adset_id = adset_id)
      adsetinsights = keysort("date", adsetinsights)
      spend = 0
      website_purchase = 0
      days = 0
      cyanprint("[%s][activedays][%s]"%(adset_id,len(adsetinsights)))
      for adsetinsight in adsetinsights:
        spend += adsetinsight.spend
        website_purchase += adsetinsight.website_purchase
        days += 1
        #input("? ? ? ? ? ? ? ? ?")
        if Adset.objects.get(adset_id=adsetinsight.adset_id).status == "ACTIVE":
          if (spend >= 20   and   website_purchase == 0):
            redprint("[stop_adsets_based_on_past_data][%s][%s][%s][%s]['!=OK']"%(adsetinsight.date, days, spend, website_purchase))
            July_Adset_Utilities().pause_adset(adset_id=adsetinsight.adset_id)
          else:
            greenprint("[%s][%s][%s][%s]['OK']"%(adsetinsight.date, days, spend, website_purchase))
  def restart_adset_based_on_today_data(self, id):
    # Goal Is Restart If Sale
    #todays_date = int(Date().myDatetimenow())
    #adsetinsights = Adsetinsight.objects.filter(date=todays_date)
    #cyanprint("[Count active today][%s]"%len(adsetinsights))
    #for adsetinsight in adsetinsights:
    #  if Adset.objects.get(adset_id=adsetinsight.adset_id).status == "PAUSED":
    #    print(adsetinsight.id, adsetinsight.website_purchase)
    #    if (adsetinsight.website_purchase > 0):
    #      redprint("[restart_adsets_based_on_today_data][%s][%s][%s] [%s]['!=OK']"%(adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
    #      July_Adset_Utilities().restart_adset(adset_id=adsetinsight.adset_id)
    #    else:
    #      greenprint("[%s][%s][%s][%s] [%s]['OK']"%(adsetinsight.id,adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
    todays_date = int(Date().myDatetimenow())
    adsetinsight = tryreturn(Get, Adsetinsight, date=todays_date)
    if(0==adsetinsight): print("No adsetinsight to restart adset on todays data with"); return
    


    print(adsetinsight.id, adsetinsight.website_purchase)
    if (adsetinsight.website_purchase > 0):
      greenprint("[restart_adsets_based_on_today_data][%s][%s][%s] [%s]['!=OK']"%(adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
      July_Adset_Utilities().restart_adset(adset_id=adsetinsight.adset_id)
    else:
      redprint("[%s][%s][%s][%s] [%s]['OK']"%(adsetinsight.id,adsetinsight.adset_id,adsetinsight.spend,adsetinsight.impression_cost,adsetinsight.website_purchase))
      todays_date = int(Date().myDatetimenow())
          
    print(adsetinsight.id, adsetinsight.website_purchase)
    adsetinsight.save()
  def update_ad_keyword_data(self, id):
    time.sleep(2)
    distinct_print("\nupdate_ad_keyword_data\n")
    fields = ["actions", "clicks", "frequency", "impressions", "reach", "spend",]
    #if (Adset.objects.get(adset_id=adset_id).date_last_requested_keyword_stats != None) and ( (int(Date().myDatetimenow()) - Adset.objects.get(adset_id=adset_id).date_last_requested_keyword_stats) < 7):
    #  # (default is 0 for date_last_requested_keyword_stats); continue if Previously requested keyword stats, and  timerange since: < 7 days. <7 since.   200 is last day requested. on 208 it will send 201-207. 208-200 = 8. 8>7.
    #  continue

    adset = Filter(Adset,adset_id=id)[0]
    adset_id = id
    if Adset.objects.get(adset_id=adset_id).date_last_requested_keyword_stats == None:
      adset = Adset.objects.get(adset_id=adset_id); adset.date_last_requested_keyword_stats = 0; adset.save()
    date_last_requested_keyword_stats_time_length = ((int(Date().myDatetimenow()-1) - Adset.objects.get(adset_id=adset_id).date_last_requested_keyword_stats))
    distinct_print("date last requested keyword stats time length: %s" % date_last_requested_keyword_stats_time_length)
    if (date_last_requested_keyword_stats_time_length >= 1) == False:
      return None
    Shop()(Adset.objects.get(adset_id=adset_id).shop_abbreviation)
    adset = AdSet(adset_id)

    ad = None
    ads = adset.get_ads()
    if len(ads) == 0:
      return
    ad = ads[0]


    q=[]
    data = []
    dates = lmap(lambda i: (Date()-i)().strftime("%Y-%m-%d"), [8,7,6,5,4,3,2])
    for i in dates:
      keyword_stats = ad.get_keyword_stats(fields=fields,params={"date":i})
      # print(keyword_stats)
      if len(keyword_stats) > 0:
        q.append(keyword_stats)
        keyword_stat = keyword_stats[0].export_all_data()
        for a in keyword_stat:
          keyword_stat[a]["date"] = Date().myDatetimenow(Date(i)())
          x = keyword_stat[a]
          distinct_print(":Keyword Stat:\nImpressions:%s, Reach: %s, Spend: %s, Date: %s, Name: %s"%(x["impressions"], x["reach"], x["spend"], x["date"], a))
        keyword_stat = AttrDict(keyword_stat)
        data.append(keyword_stat)
        #[2018.12.18 8:03:55 AM]Removed for ascii errordistinct_print("adset id, %s, len data, %s" % (adset_id, len(data)))
        #[2018.12.18 8:03:55 AM]Removed for ascii errordistinct_print(data[-1])
        print("\n\n")
        #input("continue")



    for keyword_stat in data:
      for name,values in keyword_stat.items():
        new = Interestinsight()
        existing = Interestinsight.objects.filter(adset_id = adset_id, date = values.date, interest_name = name)
        if len(existing) == 1:
          new = existing[0]
          #asciidistinct_print("[existing][adset_id][date][interest_name][%s][%s][%s]"%(adset_id,values.date,name))
          ""
        elif len(existing) == 0:
          #asciidistinct_print("[addition][adset_id][date][interest_name][%s][%s][%s]"%(adset_id,values.date,name))
          ""

        new.adset_id = adset_id
        new.date = values.date
        new.interest_name = name

        try:actions = AttrDict(keyword_stat[name]).actions
        except: actions = {}
        try:actions_dict = AttrDict(dict(zip(key("action_type", actions), key("value", actions))))
        except:actions_dict = {}

        interest_id = int(values.id)
        interest_name = name
        spend = getattr(new,"spend",0) + float(values.get("spend",0))
        reach = getattr(new,"reach",0) + int(values.get("reach",0))
        impression = getattr(new,"impression",0) + int(values.get("impressions",0))
        click = getattr(new,"click",0) + int(actions_dict.get("link_click",0))
        post_click = getattr(new,"post_click",0) + int(values.get("clicks", 0))
        add_to_cart = getattr(new,"add_to_cart",0) + int(actions_dict.get("offsite_conversion.fb_pixel_add_to_cart",0))
        website_purchase = getattr(new,"website_purchase",0) + int(actions_dict.get("offsite_conversion.fb_pixel_purchase", 0))
        page_engagement = getattr(new,"page_engagement",0) + int(actions_dict.get("page_engagement",0))
        photo_view = getattr(new,"photo_view",0) + int(actions_dict.get("photo_view",0))
        post_engagement = getattr(new,"post_engagement",0) + int(actions_dict.get("post_engagement",0))
        post_like = getattr(new,"post_like",0) + int(actions_dict.get("post_like",0))
        

        new.interest_id = interest_id
        new.interest_name = interest_name
        new.spend = spend
        new.reach = reach
        new.impression = impression
        new.click = click
        new.post_click = post_click
        new.add_to_cart = add_to_cart
        new.website_purchase = website_purchase
        new.page_engagement = page_engagement
        new.photo_view = photo_view
        new.post_engagement = post_engagement
        new.post_like  = post_like

        new.save()
      adset = Adset.objects.get(adset_id=adset_id)
      adset.date_last_requested_keyword_stats = int(Date().myDatetimenow()-1)
      #print("[%s][%s][%s]" % (adset_id, interest_name, adset.date_last_requested_keyword_stats))
      adset.save()








      #input("?: ")
  def update_adset_targeting_data(self, id):
    adset_id = id
    adset = AdSet(adset_id)
    Shop()(Adset.objects.get(adset_id=adset_id).shop_abbreviation)
    data = AttrDict(adset.remote_read(fields=["daily_budget", "created_time","effective_status","targeting","attribution_spec","promoted_object","billing_event","optimization_goal","recommendations","bid_info","name","source_adset_id"]).export_all_data())

    attribution_spec_dict = dict(zip(key("event_type", data.attribution_spec), key("window_days", data.attribution_spec)))

    flexible_spec1 = None
    flexible_spec2 = None
    flexible_spec3 = None
    flexible_spec4 = None
    flexible_spec5 = None

    created_time = datetime.strptime('-'.join(data.get("created_time").split("-")[:-1]), '%Y-%m-%dT%H:%M:%S')
    click_attribution = attribution_spec_dict.get("CLICK_THROUGH", 0)
    view_attribution = attribution_spec_dict.get("VIEW_THROUGH", 0)
    custom_event_type = data.promoted_object.custom_event_type
    billing_event = data.billing_event
    optimization_goal = data.optimization_goal
    recommendations = data.get("recommendations", "")
    bid_info = data.get("bid_info", "")
    device_platforms = list(sorted(data.targeting.get("device_platforms", [])))
    publisher_platforms = list(sorted(data.targeting.get("publisher_platforms", [])))
    facebook_positions = list(sorted(data.targeting.get("facebook_positions", [])))
    print(data)
    targeting_optimization = data.targeting.get("targeting_optimization","none")
    user_device = list(sorted(data.targeting.get("user_device", [])))
    user_os = list(sorted(data.targeting.get("user_os", [])))
    age_min = data.targeting.age_min
    age_max = data.targeting.age_max
    genders = data.targeting.get("genders", [0])[0] # 2 is F, 1 is M, 0 is Both?
    geo_locations = list(sorted(data.targeting.geo_locations.countries))
    status = data.get("effective_status")
    name = data.get("name")
    daily_budget = float(data.get("daily_budget")) / 100
    source_adset_id = data.get("source_adset_id", None)
    custom_audiences = data.targeting.get("custom_audiences", None)
    #body = Null
    #try:
    #  try:
    #    v = AdSet(adset_id).get_ads()[0].get_ad_creatives()[0].remote_read(fields=["effective_object_story_id", "body"])
    #    body = v["body"]
    #    effective_object_story_id = v["effective_object_story_id"]
    #    body_url = re.findall(r"[a-zA-Z]*.com.*",body)
    #    distinct_print(body_url)
    #
    #
    #  except:
    #    """ an error here means an ad or creative was deleted and database needs to delete adset, """
    #    magentaprint("[adset_id][%s]"%adset_id)
    #    try:mysql_delete(Adset.objects.get(id=adset_id)) # continue # ( no effective object story id )
    #    except:pass
    #  if body == Null: 0/0
    #except Exception as e:
    #  redprint(e)
    # F L E X I B L E S P E C 
    flexible_specs_ordered_list = []
    interest_dicts = {}
    """ ::: Add Friendly Part In Here, you want to save the Facebookkeywordlist for all things 1 len ::: """
    ## testing
    #return data
    #return data.targeting.flexible_spec
    ## testing
    if "flexible_spec" in data.targeting: # here add line say, only if flexible_spec in targeting
      if(1==len(data.targeting.flexible_spec)):
        x = data.targeting.flexible_spec[0]
        October_Keyword_Utilities().receive_interest_dictlist(x.get("interests"), niche=getattr(Get(Adset,adset_id=adset_id),"niche",None))
    """ ::: Add Friendly Part In Here, you want to save the Facebookkeywordlist for all things 1 len ::: """

    try:
      for idx,i in enumerate(data.targeting.flexible_spec):
        interest_dictlist = i["interests"]
        interest_dict = dict(zip(list(map(int, key("id", interest_dictlist))), list(map(str, key("name", interest_dictlist)))))
        interest_dict_id_sum = sum(list(map(int, interest_dict.keys())))
        interest_dicts[interest_dict_id_sum] = interest_dict
      for idx, id_sum in enumerate(list(sorted(interest_dicts.keys()))):
        flexible_specs_ordered_list.append(interest_dicts[id_sum])
      for idx,flexible_spec in enumerate(flexible_specs_ordered_list):
        sorted_interest_ids = list(sorted(flexible_spec.keys()))
        ordered_interests = []
        for interest_id in sorted_interest_ids:
          interest_name = flexible_spec[interest_id]
          ordered_interests.append([interest_id, interest_name])
        flexible_specs_ordered_list[idx] = ordered_interests
      if len(flexible_specs_ordered_list) > 0:
        flexible_spec1 = flexible_specs_ordered_list[0]
      if len(flexible_specs_ordered_list) > 1:
        flexible_spec2 = flexible_specs_ordered_list[1]
      if len(flexible_specs_ordered_list) > 2:
        flexible_spec3 = flexible_specs_ordered_list[2]
      if len(flexible_specs_ordered_list) > 3:
        flexible_spec4 = flexible_specs_ordered_list[3]
      if len(flexible_specs_ordered_list) > 4:
        flexible_spec5 = flexible_specs_ordered_list[4]
    except Exception as e:
      redprint("[no interests][error: %s]"%e)
    # F L E X I B L E S P E C 

    redprint("[%s][update_adset_targeting_data][created_time][%s]" % (adset["id"],created_time))
    redprint("[%s][update_adset_targeting_data][attribution_spec_dict][%s]" % (adset["id"],attribution_spec_dict))
    redprint("[%s][update_adset_targeting_data][click_attribution][%s]" % (adset["id"],click_attribution))
    redprint("[%s][update_adset_targeting_data][view_attribution][%s]" % (adset["id"],view_attribution))
    redprint("[%s][update_adset_targeting_data][custom_event_type][%s]" % (adset["id"],custom_event_type))
    redprint("[%s][update_adset_targeting_data][billing_event][%s]" % (adset["id"],billing_event))
    redprint("[%s][update_adset_targeting_data][optimization_goal][%s]" % (adset["id"],optimization_goal))
    redprint("[%s][update_adset_targeting_data][recommendations][%s]" % (adset["id"],recommendations))
    redprint("[%s][update_adset_targeting_data][bid_info][%s]" % (adset["id"],bid_info))
    redprint("[%s][update_adset_targeting_data][device_platforms][%s]" % (adset["id"],device_platforms))
    redprint("[%s][update_adset_targeting_data][publisher_platforms][%s]" % (adset["id"],publisher_platforms))
    redprint("[%s][update_adset_targeting_data][facebook_positions][%s]" % (adset["id"],facebook_positions))
    redprint("[%s][update_adset_targeting_data][targeting_optimization][%s]" % (adset["id"],targeting_optimization))
    redprint("[%s][update_adset_targeting_data][user_device][%s]" % (adset["id"],user_device))
    redprint("[%s][update_adset_targeting_data][user_os][%s]" % (adset["id"],user_os))
    redprint("[%s][update_adset_targeting_data][age_min][%s]" % (adset["id"],age_min))
    redprint("[%s][update_adset_targeting_data][age_max][%s]" % (adset["id"],age_max))
    redprint("[%s][update_adset_targeting_data][genders][%s]" % (adset["id"],genders))
    redprint("[%s][update_adset_targeting_data][geo_locations][%s]" % (adset["id"],geo_locations))
    redprint("[%s][update_adset_targeting_data][name][%s]" % (adset["id"],name))
    #redprint("[%s][update_adset_targeting_data][body][%s]" % (adset["id"],body))
    #redprint("[%s][update_adset_targeting_data][effective_object_story_id][%s]" % (adset["id"],effective_object_story_id))
    redprint("[%s][update_adset_targeting_data][daily_budget][%s]" % (adset["id"],daily_budget))
    #@[2018.12.17 12:25 AM]for ascii redprint("[%s][update_adset_targeting_data][flexible_spec1][%s]" % (adset["id"],flexible_spec1))
    #@[2018.12.17 12:25 AM]for ascii redprint("[%s][update_adset_targeting_data][flexible_spec2][%s]" % (adset["id"],flexible_spec2))
    #@[2018.12.17 12:25 AM]for ascii redprint("[%s][update_adset_targeting_data][flexible_spec3][%s]" % (adset["id"],flexible_spec3))
    #@[2018.12.17 12:25 AM]for ascii redprint("[%s][update_adset_targeting_data][flexible_spec4][%s]" % (adset["id"],flexible_spec4))
    #@[2018.12.17 12:25 AM]for ascii redprint("[%s][update_adset_targeting_data][flexible_spec5][%s]" % (adset["id"],flexible_spec5))


    adset = Adset.objects.get(adset_id=adset_id)
    adset.created_time = created_time
    adset.click_attribution = click_attribution
    adset.view_attribution = view_attribution
    adset.custom_event_type = custom_event_type
    adset.billing_event = billing_event
    adset.optimization_goal = optimization_goal
    adset.recommendations = recommendations
    adset.bid_info = dict(bid_info)
    adset.device_platforms = device_platforms
    adset.publisher_platforms = publisher_platforms
    adset.facebook_positions = facebook_positions
    adset.targeting_optimization = targeting_optimization
    adset.user_device = user_device
    adset.user_os = user_os
    adset.age_min = age_min
    adset.age_max = age_max
    adset.genders = genders
    adset.geo_locations = geo_locations
    adset.status = status
    adset.name = name
    adset.daily_budget = daily_budget
    #adset.body = body
    #adset.effective_object_story_id = effective_object_story_id
    adset.source_adset_id = source_adset_id
    adset.custom_audiences = custom_audiences
    adset.flexible_spec1 = flexible_spec1
    adset.flexible_spec2 = flexible_spec2
    adset.flexible_spec3 = flexible_spec3
    adset.flexible_spec4 = flexible_spec4
    adset.flexible_spec5 = flexible_spec5


    adset.save()
  def database_fields_to_data(self, adset_id):

    adset = Adset.objects.get(adset_id=adset_id)
    x = {}
    x = AttrDict(x)
    if adset.click_attribution:
      x.attribution_spec = [] if "attribution_spec" not in x else x.attribution_spec
      x.attribution_spec.append({'event_type': 'CLICK_THROUGH', 'window_days': adset.click_attribution})
    if adset.view_attribution:
      x.attribution_spec = [] if "attribution_spec" not in x else x.attribution_spec
      x.attribution_spec.append({'event_type': 'VIEW_THROUGH', 'window_days': adset.view_attribution})
    if adset.custom_event_type:
      x.promoted_object = {} if "promoted_object" not in x else x.promoted_object
      x.promoted_object.custom_event_type = adset.custom_event_type
      x.promoted_object.pixel_id = Shop.objects.get(shop_abbreviation = adset.shop_abbreviation).Facebook_Pixel_ID
      x.promoted_object.pixel_rule = '{"event":{"eq":"%s"}}' % adset.custom_event_type.title()
    if adset.billing_event:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.billing_event = adset.billing_event
    if adset.optimization_goal:
      x.optimization_goal = adset.optimization_goal
    if adset.recommendations:
      None
    if adset.bid_info:
      None
      redprint("[No information set on what to do in event of a bid_info field as of 7/20/18]")
    if adset.device_platforms:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.device_platforms = adset.device_platforms
    if adset.facebook_positions:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.facebook_positions = adset.facebook_positions
    if adset.publisher_platforms:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.publisher_platforms = adset.publisher_platforms
    if adset.targeting_optimization:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.targeting_optimization = adset.targeting_optimization
    if adset.user_device:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.user_device = adset.user_device
    if adset.user_os:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.user_os = adset.user_os
    if adset.age_min:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.age_min = adset.age_min
    if adset.age_max:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.age_max = adset.age_max
    if adset.genders:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.genders = [adset.genders]
    if adset.geo_locations:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.geo_locations = {'countries': adset.geo_locations, 'location_types': ['home', 'recent']} 
    if adset.status:
      x.status = adset.status
    if adset.flexible_spec1:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.flexible_spec = []
      x.targeting.flexible_spec.append({})
      x.targeting.flexible_spec[-1]["interests"] = []
      for i,j in adset.flexible_spec1:
        x.targeting.flexible_spec[-1]["interests"].append({"name":i, "id":j})
    if adset.flexible_spec2:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.flexible_spec = []
      x.targeting.flexible_spec.append({})
      x.targeting.flexible_spec[-1]["interests"] = []
      for i,j in adset.flexible_spec2:
        x.targeting.flexible_spec[-1]["interests"].append({"name":i, "id":j})
    if adset.flexible_spec3:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.flexible_spec = []
      x.targeting.flexible_spec.append({})
      x.targeting.flexible_spec[-1]["interests"] = []
      for i,j in adset.flexible_spec3:
        x.targeting.flexible_spec[-1]["interests"].append({"name":i, "id":j})
    if adset.flexible_spec4:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.flexible_spec = []
      x.targeting.flexible_spec.append({})
      x.targeting.flexible_spec[-1]["interests"] = []
      for i,j in adset.flexible_sspec4:
        x.targeting.flexible_spec[-1]["interests"].append({"name":i, "id":j})
    if adset.flexible_spec5:
      x.targeting = {} if "targeting" not in x else x.targeting
      x.targeting.flexible_spec = []
      x.targeting.flexible_spec.append({})
      x.targeting.flexible_spec[-1]["interests"] = []
      for i,j in adset.flexible_spec5:
        x.targeting.flexible_spec[-1]["interests"].append({"name":i, "id":j})
    x.targeting = dict(x.targeting)
    try:x.promoted_object = dict(x.promoted_object)
    except Exception as e:print(e)
    x = dict(x)
    return x
  def algorithm4(self,id):
    a_shop()
    adset = Get(Adset,adset_id=id)
    if adset.status=="ACTIVE":
      data = keysort("date", Adsethourlyinsight.objects.filter(adset_id=adset.adset_id), tcer=False)
      impressions = 0; sales = 0
      for x in data:

        impressions+=x.impression
        sales+=x.website_purchase


        print(impressions, sales)
        if impressions > 500:
          if sales < 1:
            print("stop")
            print("[adset_id][%s]"%adset.adset_id)
            input("please check it, impressions: %s, sales: %s" % (impressions, sales))
            AdSet(adset.adset_id).remote_update(params={"status":"PAUSED"})
            break
  def update_advertisement_all(self, id):
    # OSA.log("1")
    July_Adset_Utilities().update_adset(id=id)
    # OSA.log("2")
    July_Adset_Utilities().update_adset_targeting_data(id=id)
    # OSA.log("3")
    July_Adset_Utilities().update_adsetinsight_data(id=id)
    # OSA.log("4")
    July_Adset_Utilities().update_adsethourlyinsight_data(id=id)
    # OSA.log("5")
    July_Adset_Utilities().stop_adset_based_on_today_data(id=id)
    # OSA.log("6")
    July_Adset_Utilities().stop_adset_based_on_past_data(id=id)
    # OSA.log("7")
    July_Adset_Utilities().restart_adset_based_on_today_data(id=id)
    # OSA.log("8")
    July_Adset_Utilities().algorithm4(id=id)
    # OSA.log("I")
    July_Adset_Utilities().update_ad_keyword_data(id=id)
    # OSA.log("J")
    x = datetime.now()
    Update(Get(Adset,adset_id=id),last_check=datetime.now())
    # OSA.log("L")
    return x.strftime("%Y,%m,%d,%H,%M,%S")
  def update_advertisements(self,shop):
    for i in Filter(Adset,shop_abbreviation=shop):
      July_Adset_Utilities().update_advertisement_all(i.adset_id)
  def tests(self):
    #July_Adset_Utilities().update_adsets()
    #July_Adset_Utilities().update_adsetinsight_data(date_start = 30, date_end = 0)
    #data = CSV().pick_data(Adsetinsight.objects.all(), ["spend","adset_id","date","frequency","impression","impression_cost","impression_rate","post_click","post_click_cost","post_click_rate","click","click_cost","click_rate","add_to_cart","add_to_cart_cost","add_to_cart_rate","website_purchase","website_purchase_cost","website_purchase_rate","spend","website_purchase_value","return_on_investment","reach","reach_cost","reach_rate","landing_page_view","landing_page_view_cost","landing_page_view_rate","fb_pixel_view_content","fb_pixel_view_content_cost","fb_pixel_view_content_rate","fb_pixel_initiate_checkout","fb_pixel_initiate_checkout_cost","fb_pixel_initiate_checkout_rate","page_engagement","page_engagement_cost","page_engagement_rate","post_engagement","post_engagement_cost","post_engagement_rate","post_reaction","post_reaction_cost","post_reaction_rate"])
    #CSV().DictWriteWithHeaders("out.csv", data, headers=["spend","adset_id","date","frequency","impression","impression_cost","impression_rate","post_click","post_click_cost","post_click_rate","click","click_cost","click_rate","add_to_cart","add_to_cart_cost","add_to_cart_rate","website_purchase","website_purchase_cost","website_purchase_rate","spend","website_purchase_value","return_on_investment","reach","reach_cost","reach_rate","landing_page_view","landing_page_view_cost","landing_page_view_rate","fb_pixel_view_content","fb_pixel_view_content_cost","fb_pixel_view_content_rate","fb_pixel_initiate_checkout","fb_pixel_initiate_checkout_cost","fb_pixel_initiate_checkout_rate","page_engagement","page_engagement_cost","page_engagement_rate","post_engagement","post_engagement_cost","post_engagement_rate","post_reaction","post_reaction_cost","post_reaction_rate"])
    CSV().dictlist_to_xlsx(Adsetinsight.objects.all(), ["spend","adset_id","date","frequency","impression","impression_cost","impression_rate","post_click","post_click_cost","post_click_rate","click","click_cost","click_rate","add_to_cart","add_to_cart_cost","add_to_cart_rate","website_purchase","website_purchase_cost","website_purchase_rate","spend","website_purchase_value","return_on_investment","reach","reach_cost","reach_rate","landing_page_view","landing_page_view_cost","landing_page_view_rate","fb_pixel_view_content","fb_pixel_view_content_cost","fb_pixel_view_content_rate","fb_pixel_initiate_checkout","fb_pixel_initiate_checkout_cost","fb_pixel_initiate_checkout_rate","page_engagement","page_engagement_cost","page_engagement_rate","post_engagement","post_engagement_cost","post_engagement_rate","post_reaction","post_reaction_cost","post_reaction_rate"],
        workbook  =  ".xlsx", sheet="sheet" )

    July_Adset_Utilities().stop_adsets_based_on_today_data()
    July_Adset_Utilities().stop_adsets_based_on_past_data()
    July_Adset_Utilities().restart_adsets_based_on_today_data()
class October_Keyword_Utilities:
  #@[2018.11.23 02:44 PM][I took out the __init__ because i did print the exception in `pool` and i was not able to set the shop that many times in succession. i then got the api call must be set error and then i just set the shop in the beginning]
  t_format_ids = lambda self, ids: [{"interests": [{'id':i} for i in ids]}]
  def t_format_resp(self, resp):
    payload = []
    for i in resp:
      if i.get('valid',True) == True:
        payload.append({'id':i['id'], 'audience_size':i['audience_size'],'name':i['name'],
                        'category':i.get('disambiguation_category',''), 'topic':i.get('topic','')})
    return payload
  def receive_interest_dictlist(self, x, niche):
    """ ::: Problem: (1)Order (2)integer_ids ::: """
    """ ::: Solution: (1)integerify__forloop (2)keysort__id ::: """
    for i in x:   i["id"] = int(i["id"])
    x = keysort("id",x)
    if x not in key("keywordlist",All(Facebookkeywordlist)):
      Facebookkeywordlist(niche=niche, keywordlist=x, audience_size=October_Keyword_Utilities().re(x)).save()
  def re(self, io=None):
    if not io: return 1000000000
    ids = None
    """ ::: if io aint just ids, and its dictlist, ok, make ids the key("id"), else, ids=io(int list) ::: """
    if(type(io[0]) not in [str,int]):
      ids = key("id",io)
    else:
      ids = io
    account = AdAccount("act_%s"%(a_shop().Facebook_Business_Ad_Account_ID))
    t_spec = {'age_max': 65,
             'age_min': 18,
             'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
             'device_platforms': ['mobile', 'desktop'],
             'facebook_positions': ['feed', 'right_hand_column', 'instant_article'],
             'geo_locations': {'countries': ['US'], 'location_types': ['home']},
             'publisher_platforms': ['facebook', 'audience_network'],
             'targeting_optimization': 'none',
             'flexible_spec': []
             }
    # automatic placements
    t_spec = {'age_max': 65,
             'age_min': 18,
             'geo_locations': {'countries': ['US'], 'location_types': ['home']},
             'targeting_optimization': 'none',
             'flexible_spec': []
             }
    # added this 2nd t_spec in as this is how based on 10/2018 targeting was by default
    # t_spec = {'age_max': 65,
    #          'age_min': 18,
    #          #'audience_network_positions': ['classic', 'instream_video', 'rewarded_video'],
    #          'device_platforms': ['mobile'],
    #          'facebook_positions': ['feed'],
    #          'geo_locations': {'countries': ['US'],},
    #          'publisher_platforms': ['facebook'],
    #          'targeting_optimization': 'none',
    #          'flexible_spec': []
    #          }
    if ids:
      t_spec['flexible_spec'] = t_format_ids(ids)
    params = {
        #'currency': 'USD',
        #'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
        'targeting_spec': t_spec, }
    reach_estimate = account.get_reach_estimate(params=params)
    return reach_estimate[0]["users"]
  def t_search(self, q, limit=10000):
    resp = TargetingSearch.search(params={'q':q,'type':'adinterest','limit':limit})
    return t_format_resp(resp)
  def t_suggestion(self, names, limit=10000):
    resp = TargetingSearch.search(params={'interest_list':list(names), 'type':'adinterestsuggestion', 'limit':limit})
    return t_format_resp(resp)
  def se(self, q, limit=50):
    #@altered to achieve results with `,` or `\n`
    new = []
    for q in copy.deepcopy(q).replace("\n",",").split(","):
      x = [i for i in json.loads(requests.get(Muta()().targeting_search_url.format(q,limit)).text).get("data",[]) if("interests"==i["type"])      ]
      def pool_target(i):
        x = dict(id=int(i["id"]),name=i["name"],audience_size=Facebookkeyword.re( int(i["id"]) )  )
        return x
      if len(x) == 0:
        OSA.notify("No Results for `{}`".format(q))
        return []
      x = pool(pool_target, x, nodes=2).result()

      x = [Facebookkeyword(**i) for i in x]
      # keycall("save",x)
      for i in x: i.save()
      x = keycall("zone", x)
      new.extend(x)
    return new
  def su(self, ids, limit=50):
    targeting_list = json.dumps([{"id":i,"type":"interests"} for i in ids])
    redprint(targeting_list)
    x = [i for i in json.loads(requests.get(Muta()().targeting_suggestions_url.format(targeting_list,limit)).text).get("data",[]) if("interests"==i["type"]) ]
    def pool_target(i):
      x = dict(id=int(i["id"]),name=i["name"],audience_size=Facebookkeyword.re( int(i["id"]) )  )
      redprint("hello")
      return x
    x = pool(pool_target, x, nodes=15).result()

    x = [Facebookkeyword(**i) for i in x]
    keycall("save",x)
    #return keysort("audience_size", x)
    x = keycall("zone", x)
    return x
class AceInTheHoleHeaderColumns(Records):
  id = AutoField()
  account = CharField()
  header_column_dict = JSONField()
  active = IntegerField()
  shop = CharField()
  # :End:
  def add(self):
    shop = OSA.log("Shop that these header columns are for?: ")
    account = OSA.log("Account?: ")
    header_column_dict = {}
    headers = ["date","description","amount",]
    for i in headers:
      name = OSA.log("name for field '%s'?:"%(i))
      header_column_dict[name] = i
    Save(AceInTheHoleHeaderColumns,account=account,header_column_dict=header_column_dict,shop=shop)
class AceInTheHoleNote(Records):
  id = AutoField()
  amount = FloatField()
  note = CharField()
  date = DateField()
  # :End:
class AceInTheHoleRefund(Records):
  id = AutoField()
  amount = FloatField()
  date = DateField()
  description = CharField()
  # :End:
class AceInTheHoleType(Records):
  id = AutoField()
  name = CharField(unique=True)
  # :End:
  """ # some default types
  BUSINESS_PAYMENT_GATEWAY_DEPOSITS
  BUSINESS_PAYMENT_GATEWAY_WITHDRAWALS
  BUSINESS_PURCHASING_PRODUCTS
  BUSINESS_PURCHASING_ADS
  BUSINESS_OTHER_CONTRACT_LABOR
  BUSINESS_OTHER_HOSTING
  BUSINESS_OTHER_SUBSCRIPTIONS
  PERSONAL_NOT_FOOD
  PERSONAL_FOOD
  """
class AceInTheHoleTypeTag(Records):
  id = AutoField()
  type = CharField(max_length="0128",unique=True)
  tag = CharField(max_length="0128",unique=True)
  sign = CharField(max_length="0128",unique=True)
  # :End:
  def run_all(self):
    for i in All(AceInTheHoleTypeTag):
      AceInTheHoleTypeTag().run_tag(i.type,i.tag)
  def run_tag(self,type,tag):
    OSA.notify("STARTING %s %s"%(type,tag))
    x = Filter(AceInTheHole,tag=None,type=None,description__icontains=tag)
    sign = Get(AceInTheHoleTypeTag,type=type,tag=tag).sign
    x = ([i for i in x if i.amount>0])if(sign=="positive")else([i for i in x if i.amount<0])if(sign=="negative")else(x)if(sign=="positive_or_negative")else()
    for idx, i in enum(x):
      Update(i,type=type,tag=tag)
      OSA.notify("%s Successfully tagged for"%(idx+1),b="%s: %s"%(type,tag))
      # time.sleep(0.2)
      time.sleep(0.1)
    #OSA.notify("%s Successfully tagged for"%(len(x)+1),b="%s: %s"%(type,tag))
class Adset_duplicate(Records):
  id = AutoField()
  original_adset_id = BigIntegerField(unique=True)
  adset_ids = JSONField()
  budgets = JSONField()
  to_duplicate = BooleanField(default=False)
  duplicate_count = IntegerField()
  # :End:
  def append_adset_duplicate(self, original_adset_id=None, duplicate_count=None):
    new = Adset_duplicate()
    original_adset_id = int(redinput("original_adset_id?: ")) if original_adset_id == None else original_adset_id
    duplicate_count = int(redinput("duplicate_count?: ")) if duplicate_count == None else duplicate_count
    existing = Adset_duplicate.objects.filter(original_adset_id = original_adset_id)
    if len(existing) == 0:
      existing = [adset_duplicate for adset_duplicate in Adset_duplicate.objects.all() if original_adset_id in adset_duplicate.adset_ids]
      if len(existing) > 0:
        assert len(existing) == 1
        redprint("[original adset id was a duplicate adset id]")
      else:
        redprint("[original adset id does not exist]")
    elif len(existing) == 1:
      redprint("[original adset id exists]")
      new = existing[0]
    new.duplicate_count = duplicate_count
    new.to_duplicate = True
    new.budgets = []
    new.adset_ids = []
    new.original_adset_id = original_adset_id
    new.save()
    distinct_print(ordered_json_dumps(new.__dict__))
class Adsethourlyinsight(Records):
  id = AutoField()
  ad_account_id = BigIntegerField()
  adset_id = BigIntegerField(unique=True)
  date = FloatField(unique=True)
  frequency = FloatField()
  impression = IntegerField()
  impression_rate = FloatField()
  impression_cost = FloatField()
  post_click = IntegerField()
  post_click_cost = FloatField()
  post_click_rate = FloatField()
  click = IntegerField()
  click_cost = FloatField()
  click_rate = FloatField()
  add_to_cart = IntegerField()
  add_to_cart_cost = FloatField()
  add_to_cart_rate = FloatField()
  website_purchase = IntegerField()
  offsite_conversion = IntegerField()
  website_purchase_cost = FloatField()
  website_purchase_rate = FloatField()
  spend = FloatField()
  website_purchase_value = FloatField()
  return_on_investment = FloatField()
  reach = IntegerField()
  reach_cost = FloatField()
  reach_rate = FloatField()
  landing_page_view = IntegerField()
  landing_page_view_cost = FloatField()
  landing_page_view_rate = FloatField()
  fb_pixel_view_content = IntegerField()
  fb_pixel_view_content_cost = FloatField()
  fb_pixel_view_content_rate = FloatField()
  fb_pixel_initiate_checkout = IntegerField()
  fb_pixel_initiate_checkout_cost = FloatField()
  fb_pixel_initiate_checkout_rate = FloatField()
  page_engagement = IntegerField()
  page_engagement_cost = FloatField()
  page_engagement_rate = FloatField()
  post_engagement = IntegerField()
  post_engagement_cost = FloatField()
  post_engagement_rate = FloatField()
  post_reaction = IntegerField()
  post_reaction_cost = FloatField()
  post_reaction_rate = FloatField()
  order_ids = JSONField()
  # :End:
class Adsethourlyinsightdata(Records):
  id = AutoField()
  ad_account_id = BigIntegerField()
  adset_id = BigIntegerField(unique=True)
  date = FloatField(unique=True)
  
  spend = FloatField()
  website_purchase_value = FloatField()

  impression_move = IntegerField()
  post_click_move = IntegerField()
  click_move = IntegerField()
  add_to_cart_move = IntegerField()
  website_purchase_move = IntegerField()
  reach_move = IntegerField()
  landing_page_view_move = IntegerField()
  fb_pixel_view_content_move = IntegerField()
  fb_pixel_initiate_checkout_move = IntegerField()
  page_engagement_move = IntegerField()
  post_engagement_move = IntegerField()
  post_reaction_move = IntegerField()

  impression_adspendvg = FloatField()
  post_click_adspendvg = FloatField()
  click_adspendvg = FloatField()
  add_to_cart_adspendvg = FloatField()
  website_purchase_adspendvg = FloatField()
  reach_adspendvg = FloatField()
  landing_page_view_adspendvg = FloatField()
  fb_pixel_view_content_adspendvg = FloatField()
  fb_pixel_initiate_checkout_adspendvg = FloatField()
  page_engagement_adspendvg = FloatField()
  post_engagement_adspendvg = FloatField()
  post_reaction_adspendvg = FloatField()

  impression_ratevg = FloatField()
  post_click_ratevg = FloatField()
  click_ratevg = FloatField()
  add_to_cart_ratevg = FloatField()
  website_purchase_ratevg = FloatField()
  reach_ratevg = FloatField()
  landing_page_view_ratevg = FloatField()
  fb_pixel_view_content_ratevg = FloatField()
  fb_pixel_initiate_checkout_ratevg = FloatField()
  page_engagement_ratevg = FloatField()
  post_engagement_ratevg = FloatField()
  post_reaction_ratevg = FloatField()

  frequency = FloatField()
  offsite_conversion = IntegerField()
  return_on_investment = FloatField()

  order_ids = JSONField()

  name = CharField()
  niche = CharField()
  shop_abbreviation = CharField()
  facebook_page = CharField()
  product_url = CharField()
  image_url = CharField()
  caption = JSONField()
  complete_create = BooleanField(default=False)
  is_created = BooleanField(default=False)
  campaign_id = BigIntegerField()
  created_time = DateTimeField()
  date_last_requested_keyword_stats = IntegerField()
  click_attribution = IntegerField()
  view_attribution = IntegerField()
  custom_event_type = CharField()
  billing_event = CharField()
  optimization_goal = CharField()
  recommendations = CharField()
  bid_info = JSONField()
  bid_strategy = CharField()
  device_platforms = JSONField()
  publisher_platforms = JSONField()
  facebook_positions = JSONField()
  targeting_optimization = CharField()
  user_device = JSONField()
  user_os = JSONField()
  age_min = IntegerField()
  age_max = IntegerField()
  genders = IntegerField()
  geo_locations = JSONField()
  status = CharField()
  name = CharField()
  daily_budget = FloatField()
  body = JSONField()
  effective_object_story_id = CharField()
  source_adset_id = BigIntegerField()
  custom_audiences = JSONField()
  flexible_spec1 = JSONField()
  flexible_spec2 = JSONField()
  flexible_spec3 = JSONField()
  flexible_spec4 = JSONField()
  flexible_spec5 = JSONField()
  notes = JSONField()
  # :End:
class Adsetinsight(Records):
  id = AutoField()
  ad_account_id = BigIntegerField()
  adset_id = BigIntegerField(unique=True)
  date = IntegerField(unique=True)
  frequency = FloatField()
  impression = IntegerField()
  impression_rate = FloatField()
  impression_cost = FloatField()
  post_click = IntegerField()
  post_click_cost = FloatField()
  post_click_rate = FloatField()
  click = IntegerField()
  click_cost = FloatField()
  click_rate = FloatField()
  add_to_cart = IntegerField()
  add_to_cart_cost = FloatField()
  add_to_cart_rate = FloatField()
  website_purchase = IntegerField()
  website_purchase_cost = FloatField()
  website_purchase_rate = FloatField()
  spend = FloatField()
  website_purchase_value = FloatField()
  return_on_investment = FloatField()
  reach = IntegerField()
  reach_cost = FloatField()
  reach_rate = FloatField()
  landing_page_view = IntegerField()
  landing_page_view_cost = FloatField()
  landing_page_view_rate = FloatField()
  fb_pixel_view_content = IntegerField()
  fb_pixel_view_content_cost = FloatField()
  fb_pixel_view_content_rate = FloatField()
  fb_pixel_initiate_checkout = IntegerField()
  fb_pixel_initiate_checkout_cost = FloatField()
  fb_pixel_initiate_checkout_rate = FloatField()
  page_engagement = IntegerField()
  page_engagement_cost = FloatField()
  page_engagement_rate = FloatField()
  post_engagement = IntegerField()
  post_engagement_cost = FloatField()
  post_engagement_rate = FloatField()
  post_reaction = IntegerField()
  post_reaction_cost = FloatField()
  post_reaction_rate = FloatField()
  order_ids = JSONField()
  # :End:
class Audience(Records):
  id = AutoField()
  name = CharField()
  pcs = DecimalField()
  roi = DecimalField()
  spent = DecimalField()
  pcv = DecimalField()
  flex = JSONField()
  state = IntegerField()
  fb_page_id = CharField()
  niche = CharField()
  objects = BaseModelManager()
  # :End:
class Content(Records):
  id = AutoField()
  content_type = CharField()
  text = BinaryField()
  page_name = CharField()
  collection_name = CharField()
  # :End:
  def __call__(self):
    process(lambda:self.get_one_content(page_name=Muta()().page))
  def add_content(self):
    page_name, content_type = OSA.log("page name, content type separated by ', '?").split(", ")
    content = OSA.log("Content?\n1234567891234567891234567891234567891234567\n%s"%("|"*80),df="\n\n\n\n\n\n\n\n\n",buttons=["Cancel","OK"])
    Save(Content,content_type=content_type,page_name=page_name,text=content)
  def add_content_from_csv(self,infile):
    data = CSV().DictRead(infile,delimiter=",")
    for row in data:
      page_name = row["page_name"]
      content_type = row["content_type"]
      content = row["content"].encode()
      collection_name = row["name"]
      if content not in key("text",Filter(Content,page_name=page_name)):
        print(page_name, content_type)
        print(content.decode(), "\n\n")
        Save(Content,page_name=page_name,content_type=content_type,text=content,collection_name=collection_name)
  def get_one_content(self,page_name):
    content, image = Content().generate_content(page_name=page_name,count=1)
    content, image = content[0], image[0]
    impreview(Images().download(image))
    text_to_image(content)
  def get_one_content(self,page_name):
    item = get_random_from_lists(0.3,0.7,Filter(Content,content_type="Collection_Sales",page_name=page_name),Filter(Content,content_type="Collection_Sales",page_name=page_name))
    collection_name = item.collection_name

    content_link = random.choice(Filter(Content_Link,page_name=page_name,collection_name=collection_name))
    collection_name_unpluralized, collection_link = content_link.collection_name_unpluralized, content_link.collection_url

    content_image = random.choice(Filter(Content_Image,page_name=page_name,collection_name=collection_name))
    import numpy as np
    #while content_image.url in sud("url",Filter(Content_Image,used_times__gte=1)) or\
    #      set(np.array(Images().get_image_size(Images().download(content_image.url))) < 700) == {True} or\
    #      True in set(np.array(Images().get_image_size(Images().download(content_image.url))) > 2500): content_image = random.choice(Filter(Content_Image,page_name=page_name,collection_name=collection_name))
    
    while True:
      image_used = content_image.url in sud("url",Filter(Content_Image,used_times__gte=1))
      both_sides_less_than_700 = set(np.array(Images().get_image_size(Images().download(content_image.url))) < 700) == {True}
      one_side_greater_than_2500 = True in set(np.array(Images().get_image_size(Images().download(content_image.url))) > 2500)
      if image_used: OSA.notify("image used")
      if both_sides_less_than_700: OSA.notify(a=Date().friendlydate(Date().Now(),seconds=True),b="both sides less than 700")
      if one_side_greater_than_2500: OSA.notify(a=Date().friendlydate(Date().Now(),seconds=True),b="one side greater than 2500")
      if image_used or both_sides_less_than_700 or one_side_greater_than_2500:
        content_image = random.choice(Filter(Content_Image,page_name=page_name,collection_name=collection_name))
      else:
        break

    content = item.text.decode()
    content = content.replace("<collection_name>",collection_name).replace("<collection_name_unpluralized>",collection_name_unpluralized).replace("<ru>",collection_link)
    content = content.replace("<referral_link>",content_image.source)

    impreview(Images().download(content_image.url))
    tp(lambda:text_to_image(content))

    if OSA.log("Create your own caption?",buttons=["No","Yes"],tp=False) == "Yes":
      content = OSA.log("Caption?",df="\n\n\n\n\n\n")
      content = content.replace("<ru>",collection_link)
      tp(lambda:text_to_image(content))

    to_post = OSA.log("To post?",buttons=["No","Yes"],tp=False)
    if to_post == "Yes":
      content_image.used_times += 1
      content_image.save()
      if item.content_type == "Message": ( Del(item), OSA.notify(a="Deleting Message",b=content) )
      Content().post_next_content(content, content_image.url, page_name)
    OSA().exit_preview_windows()
    return content, content_image.url
  def post_next_content(self, content, image, page_name):
    page = Get(Facebookpage,name=page_name)
    scheduled_posts = get_scheduled_posts(page_name)
    next_scheduled_time_timestamp = get_next_scheduled_time(page,scheduled_posts)
    
    OSA.notify("Running, %s" % (Date().friendlydate(datetime.now(),seconds=True)))
    page = Get(Facebookpage, name = page_name)
    token = page.token
    published = False
    image = Images().download(image)
    url = Images().fb_image_upload(image)
    page_id = page.facebook_id
    
    post_url = "https://graph.facebook.com/%s/photos"%(page_id)
    caption = content
    params = dict(access_token=token,caption=caption,published=published,url=url,scheduled_publish_time=next_scheduled_time_timestamp)
    r = requests.post(post_url,params=params)
    OSA.notify(str(r.status_code))
    OSA.notify("Complete, %s" % (Date().friendlydate(datetime.now(),seconds=True)))
    time.sleep(1)
class Content_Image(Records):
  id = AutoField()
  source = CharField(unique=True,max_length="0128")
  url = CharField(unique=True)
  page_name = CharField()
  collection_name = CharField(unique=True,max_length="0128")
  used_times = IntegerField()
  # :End:
  def add_content_images(self,urls,source,page_name,collection_name):
    lmap(lambda url: Save(Content_Image,url=url,source=source,page_name=page_name,collection_name=collection_name),urls)
class Content_Link(Records):
  id = AutoField()
  page_name = CharField(unique=True)
  collection_name = CharField(unique=True,max_length="0128")
  collection_name_unpluralized = CharField()
  collection_url = CharField()
  # :End:
  def add(self,page_name,collection_name,collection_name_unpluralized,collection_url):
    Save(Content_Link,page_name=page_name,collection_name=collection_name,collection_name_unpluralized=collection_name_unpluralized,collection_url=collection_url)
class Facebookadaccountspend(Records):
  id = AutoField()
  date = DateField(unique=True)
  ad_account_id = BigIntegerField(unique=True)
  facebookadaccountspend = FloatField()
  # :End:
  @staticmethod
  def facebookadaccountspend_source(date):
    ()if(Date(date)<Date())else(([OSA.log("Can only get adspend for previous dates",tp=0),(0/0)]))
    return ([[Facebookadaccountspend(date=date,facebookadaccountspend=i["spend"],ad_account_id=i["ad_account_id"]).save(),Get(Facebookadaccountspend, date=date,facebookadaccountspend=i["spend"],ad_account_id=i["ad_account_id"] )][1] for i in [[setitem(g(),"A",ad_account.get_insights(fields=["spend"], params={"time_range":{"since":Date(date).datestr,"until":Date(date).datestr}  }  )),{"spend":0,"ad_account_id":ad_account["account_id"]} if(0==len(g()["A"])) else [setitem(g()["A"][0],"ad_account_id",ad_account["account_id"]), g()["A"][0]] [1] ][1]         for ad_account in  get_user().get_ad_accounts()]])if(len(Filter(Facebookadaccountspend,date__range=[(Date(date).str()),(Date(date).str())]))==0)else(Filter(Facebookadaccountspend,date__range=[(Date(date).str()),(Date(date).str())]))
class Facebookimageupload(Records):
  id = AutoField()
  origin = CharField(max_length="0512",unique=True)
  destination = CharField(max_length="8192")
  # :End:
  @staticmethod
  def facebookimageupload(origin):
    try: return [Get(Facebookimageupload, origin=origin).destination,redprint("Exists: %s" % origin)][0]
    except: "pas"
    magentaprint("Saving: %s" % origin)
    origin = origin
    destination = Images().fb_image_upload(origin)
    Facebookimageupload(origin=origin,destination=destination).save()
    Get(Facebookimageupload, origin= origin)
    return destination
class Facebookkeyword(Records):
  id = BigIntegerField(primary_key=True)
  name = CharField()
  audience_size = BigIntegerField()
  # :End:
  def zone(self):
    return AttrDict({"id":self.id,"name":self.name,"audience_size":self.audience_size})
  def se(self,kw):
    October_Keyword_Utilities().se(kw)
  @staticmethod
  def re(id):
    print("checking the database...")
    checking_the_database=Filter(Facebookkeyword,id=id)
    if(0!=len(checking_the_database)):return(getitem(checking_the_database,0).audience_size)
    print("reach estimate seraching for [id]")
    audience_size = October_Keyword_Utilities().re([id])
    return audience_size
class Facebookkeywordlist(Records):
  id = AutoField()
  keywordlist = JSONField()
  audience_size = JSONField()
  niche = CharField()
  purchases = IntegerField()
  # :End:
class Facebookpage(Records):
  id = AutoField()
  facebook_id = BigIntegerField(unique=True)
  name = CharField(max_length="0032")
  url = CharField(max_length="0128")
  settings = JSONField()
  publish_times = JSONField()
  token = CharField()
  c = lambda self: AttrDict(self.settings)
  ct = lambda self, field, value: [setitem(self.settings,field,value),Update(self,settings=self.settings),self][2]
  # :End:
  def guided_create_Facebookpage(self): # Of course, you will have to authenticate time each
    facebook_id = int(input("Facebook id: "))
    name = input("Name?: ")
    url = input("url?: ")
    new = Facebookpage()
    new.facebook_id = facebook_id
    new.name = name
    new.url = url
    new.save()
  def create_facebook_post(self, page_name):
    OSA.notify("Running, %s" % (Date().friendlydate(datetime.now(),seconds=True)))
    page = Get(Facebookpage, name = page_name)
    token = page.token
    published = False
    image = get_latest_download()
    url = Images().fb_image_upload(image)
    page_id = page.facebook_id
    scheduled_posts = get_scheduled_posts(page_name)
    
    next_scheduled_time_timestamp = get_next_scheduled_time(page,scheduled_posts)

    post_url = "https://graph.facebook.com/%s/photos"%(page_id)
    caption = OSA.log("Caption?\n1234567891234567891234567891234567891234567\n%s"%("|"*80),df="\n\n\n\n\n\n\n\n\n",buttons=["Cancel","OK"])
    params = dict(access_token=token,caption=caption,published=published,url=url,scheduled_publish_time=next_scheduled_time_timestamp)
    r = requests.post(post_url,params=params)
    OSA.notify(str(r.status_code))
    OSA.notify("Complete, %s" % (Date().friendlydate(datetime.now(),seconds=True)))
class Interest(Records):
  id = AutoField()
  interest_id = BigIntegerField(unique=True)
  interest_name = CharField(max_length="0256",unique=True)
  spend = FloatField()
  reach = IntegerField()
  impression = IntegerField()
  click = IntegerField()
  post_click = IntegerField()
  add_to_cart = IntegerField()
  website_purchase = IntegerField()
  page_engagement = IntegerField()
  photo_view = IntegerField()
  post_engagement = IntegerField()
  post_like = IntegerField()
  # :End:
class Interestinsight(Records):
  id = AutoField()
  interest_id = BigIntegerField()
  interest_name = CharField(max_length="0256",unique=True)
  date = IntegerField(unique=True,default=None)
  adset_id = CharField(unique=True, max_length="0032")
  spend = FloatField()
  reach = IntegerField()
  impression = IntegerField()
  click = IntegerField()
  post_click = IntegerField()
  add_to_cart = IntegerField()
  website_purchase = IntegerField()
  page_engagement = IntegerField()
  photo_view = IntegerField()
  post_engagement = IntegerField()
  post_like = IntegerField()
  # :End:
class Adset(Worksheet):
  id = AutoField()
  last_check = DateTimeField()
  niche = CharField()
  shop_abbreviation = CharField()
  facebook_page = CharField()
  product_url = CharField()
  image_url = CharField()
  caption = JSONField()
  complete_create = BooleanField(default=False)
  icon = CharField()
  is_created = BooleanField(default=False)
  ad_account_id = BigIntegerField()
  campaign_id = BigIntegerField(unique=True)
  adset_id = BigIntegerField(unique=True)
  created_time = DateTimeField()
  date_last_requested_keyword_stats = IntegerField()
  click_attribution = IntegerField()
  view_attribution = IntegerField()
  custom_event_type = CharField()
  billing_event = CharField()
  optimization_goal = CharField()
  recommendations = CharField()
  bid_info = JSONField()
  device_platforms = JSONField()
  publisher_platforms = JSONField()
  facebook_positions = JSONField()
  targeting_optimization = CharField()
  user_device = JSONField()
  user_os = JSONField()
  age_min = IntegerField()
  age_max = IntegerField()
  genders = IntegerField()
  geo_locations = JSONField()
  status = CharField()
  name = CharField()
  daily_budget = FloatField()
  body = JSONField()
  effective_object_story_id = CharField()
  source_adset_id = BigIntegerField()
  custom_audiences = JSONField()
  original_caid = BigIntegerField()
  interest_ids = JSONField()
  flexible_spec1 = JSONField()
  flexible_spec2 = JSONField()
  flexible_spec3 = JSONField()
  flexible_spec4 = JSONField()
  flexible_spec5 = JSONField()
  handle = CharField()
  # :End:
  def Update(self):
    lmap(lambda i: July_Adset_Utilities().update_advertisement_all(id=i.id),All(Adset))
  def reach_estimate(self):
    a_shop()
    return October_Keyword_Utilities().re(key("id",flatten(key("interests",AdSet(self.adset_id).remote_read(fields=["targeting"])._json["targeting"]["flexible_spec"]),1)))
    # return AdSet(self.adset_id).get_delivery_estimate()
  def get_delivery_estimate(self):
    a_shop()
    x = AdSet(self.adset_id).get_delivery_estimate()[0]._json["estimate_mau"]
    return x
  def re(self):
    interest_ids = self.interest_ids
    audience_size = None
    try:audience_size = [i for i in All(Facebookkeywordlist) if list(sorted(key("id",i.keywordlist))) == list(sorted(interest_ids))][0].audience_size
    except Exception as e: redprint(e)
    return audience_size
    """
    keycall("re", All(Adset))
    """
  def Icon(self):
    if self.image_url == Null:
      Shop()(All(Shop)[0].shop_abbreviation)
      url = AdSet(self.adset_id).get_ads()[0].get_ad_creatives()[0].remote_read(fields=["thumbnail_url"])["thumbnail_url"]
      Update(self,image_url = url)
      redprint("Retrieved image url: %s" % self.image_url)

    os.makedirs(userfolder("~/tavern/tavern/bag/.adset_icon_images"),exist_ok=True)
    if self.icon == None:
      address = userfolder("~/tavern/tavern/bag/.adset_icon_images/no.%s.png"%self.adset_id)
      try:
        Images().download(self.image_url,save_path=address)
      except Exception as e:
        redprint(e)
        url = AdSet(self.adset_id).get_ads()[0].get_ad_creatives()[0].remote_read(fields=["thumbnail_url"])["thumbnail_url"]
        Update(self,image_url = url)
        redprint("Retrieved image url: %s" % self.image_url)
        Images().download(self.image_url,save_path=address)
      Update(self,icon=address)
      assert os.path.exists(address)                                                                                                                                                            ;redprint("self.icon: %s" % self.icon)
    if self.icon != None:
      if os.path.exists(self.icon) == False:
        address = userfolder("~/tavern/tavern/bag/.adset_icon_images/no.%s.png"%self.adset_id)
        try:
          Images().download(self.image_url,save_path=address)
        except Exception as e:
          redprint(e)
          url = AdSet(self.adset_id).get_ads()[0].get_ad_creatives()[0].remote_read(fields=["thumbnail_url"])["thumbnail_url"]
          Update(self,image_url = url)
          redprint("Retrieved image url: %s" % self.image_url)
          Images().download(self.image_url,save_path=address)
        Update(self,icon=address)
        assert os.path.exists(address)                                                                                                                                                            ;redprint("self.icon: %s" % self.icon)
    return self.icon
  def post_duplicate(self):
    a = [idx for idx,i in enum(pool(lambda i:[i.custom_audiences,i.flexible_spec1,i.flexible_spec2,i.flexible_spec3,i.flexible_spec4,i.flexible_spec5,],Filter(Adset,handle=self.handle)).result()) if i==[self.custom_audiences,self.flexible_spec1,self.flexible_spec2,self.flexible_spec3,self.flexible_spec4,self.flexible_spec5,]]
    b = [Filter(Adset,handle=self.handle)[i] for i in a]
    c = key("daily_budget",b)
    d = max(c)+5
    e = None
    if len([i for i in b if not i.original_caid and not i.source_adset_id]) > 0:
      e = [i for i in b if not i.original_caid and not i.source_adset_id][0]
      # Basically, There are two events:  I am duplicating an original, so i say please; handlized; caidless, and no source_adset_id (no duplicate) | 2: I am duplicating a Lookalike. it'll definitely have a source_adset_id lol. go below. (then, it will have an original custom audience id, the only one with an original custom audience id the original lookalike, not any duplicates of that one.)
    elif len([i for i in b if not i.original_caid and not i.source_adset_id]) == 0:
      e = [i for i in b if i.original_caid][0]
      # Basically, There are two events:  I am duplicating an original, so i say please; handlized; caidless, and no source_adset_id (no duplicate) | 2: I am duplicating a Lookalike. it'll definitely have a source_adset_id lol. go below. (then, it will have an original custom audience id, the only one with an original custom audience id the original lookalike, not any duplicates of that one.)
    f = Copy(e.adset_id)[0]
    g = itemcopy(Adset(),e,f=["niche","shop_abbreviation","facebook_page","product_url","caption","icon","is_created","ad_account_id","campaign_id","date_last_requested_keyword_stats","click_attribution","view_attribution","custom_event_type","billing_event","optimization_goal","recommendations","bid_info","device_platforms","publisher_platforms","facebook_positions","targeting_optimization","user_device","user_os","age_min","age_max","genders","geo_locations","body","effective_object_story_id","interest_ids","handle"])
    h = Update(g,adset_id=f)
    AdSet(f).remote_update(params={"daily_budget":str((d*100)) })
    July_Adset_Utilities().update_advertisement_all(f)
  def post_handle(self):
    if not self.handle:
      Update(self,handle=get_url_from_body([Shop()(All(Shop)[0].shop_abbreviation),AdSet(self.adset_id)][1].get_ads()[0].get_ad_creatives()[0].remote_read(fields=["body"])["body"]).split("/")[-1].split("?")[0])
    handle = self.handle
    custom = CustomAudience(parent_id='act_%s' %Shop()(self.shop_abbreviation).Facebook_Business_Ad_Account_ID).remote_create(params={'pixel_id': Shop()(self.shop_abbreviation).Facebook_Pixel_ID,'retention_days':'180',
        'rule':json.dumps({'inclusions': {'operator': 'or',
          'rules': [{'event_sources': [{'id': Get(Shop,shop_abbreviation=Muta()().store_abbre).Facebook_Pixel_ID, 'type': 'pixel'}],
            'filter': {'filters': [{'filters': [{'field': 'url',
                 'operator': 'i_contains',
                 'value': "/%s"%handle}],
               'operator': 'or'},
              {'field': 'url', 'operator': 'i_contains', 'value': ''}],
             'operator': 'and'},
            'retention_seconds': 15552000,
            'template': 'VISITORS_BY_URL'}]}}),
            'name':"/%s"%handle,})['id'] if not Filter(Handle,handle=handle) else 1
    Save(Handle,handle=handle,custom_audience_id=custom,has_adset=[],shop=self.shop_abbreviation)() if not Filter(Handle,handle=handle) else 1
    return custom if not Filter(Handle,handle=handle) else 1
  def i(self):
    return sudsort("date",Filter(Adsetinsight,adset_id=self.adset_id),tcer=False)


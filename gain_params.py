def calculate_return_list(img):

    img_origin = img

    #単位を求める'(nm/px)141は点の端から端まで
    scale = 200
    nm_p_px = scale/141
    img_arr = np.array(img_origin)
    img_arr = img_arr[70:428]
    blur = cv2.GaussianBlur(src = img_arr, ksize = (7,7),sigmaX = 0)

    if scale >= 200:
        img_o = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,101,0)
        kernel = np.ones((2,2),np.uint8)
        img_o_open = cv2.morphologyEx(img_o, cv2.MORPH_OPEN, kernel)
        img_o_open_close = cv2.morphologyEx(img_o_open, cv2.MORPH_CLOSE, kernel)
        input_img  = img_o_open_close.copy()
    if scale < 200:
        ret_o,img_o = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        img_o_open = cv2.morphologyEx(img_o, cv2.MORPH_OPEN, kernel)
        img_o_open_close = cv2.morphologyEx(img_o_open, cv2.MORPH_CLOSE, kernel)
        input_img  = img_o_open_close.copy()


    cnt, _ = cv2.findContours(input_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img_cnt = cv2.drawContours(input_img, cnt, -1, (25,25,0), 2)



    #面積、円形度、等価直径を求める。
    Areas = []
    Circularities = []
    Eq_diameters = []

    return_hist = []

    zero = 0
    for i in cnt:
        #面積(px*px)
        area = cv2.contourArea(i)
        if scale < 200 and area < 10:
            zero += 1
            continue

        if scale >= 200 and area == 0 :
            zero += 1
            continue
        Areas.append(area)

        #円形度
        arc = cv2.arcLength(i, True)
        circularity = 4 * np.pi * area / (arc * arc)
        Circularities.append(circularity)

        #等価直径(px)
        eq_diameter = np.sqrt(4*area/np.pi)
        Eq_diameters.append(eq_diameter)

    Areas1 = np.array(Areas)*nm_p_px**2
    Eq_diameters1 = np.array(Eq_diameters)*nm_p_px

    a =8
    fig_hist = plt.figure(figsize=(8,2.5))
    hist1 = fig_hist.add_subplot(1,3,1)
    hist1.set_title("Areas (nm^2)",fontsize=a)
    hist1.hist(Areas1, bins=25, range=(0,Areas1.max()), rwidth=0.7)
    hist1.tick_params(labelsize=a-2)

    hist2 = fig_hist.add_subplot(1,3,2)
    hist2.set_title("Circularity",fontsize=a)
    hist2.hist(Circularities, bins=25, range=(0.5,1), rwidth=0.7)
    hist2.tick_params(labelsize=a-2)

    hist3 = fig_hist.add_subplot(1,3,3)
    hist3.set_title("Equal Diameters (nm)",fontsize=a)
    hist3.hist(Eq_diameters1, bins=25, range=(0.0, Eq_diameters1.max()), rwidth=0.7)
    hist3.tick_params(labelsize=a-2)

    n_particle = len(Areas1)
    filling_rate = np.array(Areas).sum()/(img_arr.shape[0]*img_arr.shape[1])
    areas_average = np.array(Areas1).mean()
    areas_var = np.var(np.array(Areas1))
    Circularities_mean = np.array(Circularities).mean()
    Circularities_var = np.var(np.array(Circularities))
    area = np.array(img_origin).shape[0]*np.array(img_origin).shape[1]*nm_p_px**2



    particle_dataframe = pd.DataFrame(np.array([Areas,Circularities,Eq_diameters]).T,columns =  ["Areas","Circularities","Eq_diameters"])


    return_list = [scale,n_particle,filling_rate,areas_average,areas_var,Circularities_mean,Circularities_var,area]
    return np.array(return_list) , [[img_o_open_close],[img_arr]] , fig_hist , particle_dataframe

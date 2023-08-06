
import numpy as np
import copy

def bilinear(y,  x, yul, xul, vul,yur,  xur, vur, ydl, xdl, vdl, ydr,  xdr,vdr):
    u = linear(x, xul, vul, xur, vur)
    yu = linear(x, xul, yul, xur, yur)
    b = linear(x, xdl, vdl, xdr, vdr)
    yb = linear(x, xdl, ydl, xdr, ydr)
    v = linear(y, yu, u, yb, b)
    return v


def linear(x, xl, vl0, xr, vr0):
    vl=vl0
    vr=vr0
    if vl == vr:
        v=vl
    else:
        dxl = x - xl
        drl = xr - xl
        v = dxl * (vr - vl) / drl + vl
    return v

def getPoint3D(pre,df,lat0,lon0,resolution,decimal=1):
   
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[:, latIdx, lonIdx].round(decimals=decimal)


def getPoint2D(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[latIdx, lonIdx].round(decimals=decimal)

def getPointBilinear3D(preData,df1,latArr,lonArr,decimal=2):
    df=copy.copy(df1)
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[:, latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[:, latIdxS, lonIdxE]
    df["valNE"] = preData[:, latIdxN, lonIdxE]
    df["valSW"] = preData[:, latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)


def getPointBilinear2D(preData,df1,latArr,lonArr,decimal=2):
    df=copy.copy(df1)
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[ latIdxS, lonIdxE]
    df["valNE"] = preData[ latIdxN, lonIdxE]
    df["valSW"] = preData[ latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)

def classify1h(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre < 0.1] = 0
    pre[np.logical_and(pre >= 0.1, pre <= 2.5)] = 1
    pre[np.logical_and(pre > 2.5, pre <= 8)] = 2
    pre[np.logical_and(pre > 8, pre <= 16)] = 3
    pre[np.logical_and(pre > 16, pre <= 9990)] = 4
    pre[pre > 9990] = -1
    pre[np.isnan(pre)] = -1
    return pre

# classify 3h
def classify3h(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre < 0.1] = 0
    pre[np.logical_and(pre >= 0.1, pre <= 3)] = 1
    pre[np.logical_and(pre > 3, pre <= 10)] = 2
    pre[np.logical_and(pre > 10, pre <= 20)] = 3
    pre[np.logical_and(pre > 20, pre <= 9990)] = 4
    pre[pre > 9990] = -1
    pre[np.isnan(pre)] = -1
    return pre


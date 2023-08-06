def exclude_equiv_points(k_list,new_points=None):
    k_list_copy=deepcopy(k_list)
    # exclude_equiv_points_slow(k_list_copy,new_points)
    return exclude_equiv_points_fast(k_list,new_points)
#    return exclude_equiv_points_slow(k_list_copy,new_points)
#    exit()
#    return cnt


def exclude_equiv_points_slow(k_list,new_points=None):
    print ("Excluding symmetry-equivalent points-slow")
#    print ("kpoints are : \n"+"\n".join(str(k.k) for k in k_list) )
    t0=time()
    cnt=0
    n=len(k_list)
#    print (n,new_points)
#    print (-1 if new_points is None else max(-1,n-1-new_points))
    exclude=[]
    for i in range(n-1,-1 if new_points is None else max(-1,n-1-new_points),-1):
#        print (i)
        for j in range(i-1,-1,-1):
            ki=k_list[i]
            kj=k_list[j]
            if ki.equiv(kj):
                if ki.equiv(kj):
                    kj.absorb(ki)
                    exclude.append(j)
                    cnt+=1
                    del k_list[i]
                    break
#    print ("EXCLUDED ARE: ",sorted(exclude))
    print ("Done. Excluded  {} points in {} sec".format(cnt,time()-t0))
    return cnt

# this should be a faster implementation
def exclude_equiv_points_fast(k_list,new_points=None):
    print ("Excluding symmetry-equivalent points-fast")
#    print ("kpoints are : \n"+"\n".join(str(k.k) for k in k_list) )
    t0=time()
    cnt=0
    n=len(k_list)
    
    corners=np.array([[x,y,z] for x in (0,1) for y in (0,1) for z in (0,1)])
    k_list_length=np.array([ np.linalg.norm(((k.k%1)[None,:]-corners).dot(k.symgroup.basis),axis=1).min()  for k in k_list])
    k_list_sort=np.argsort(k_list_length)
    k_list_length=k_list_length[k_list_sort]
    wall=[0]+list(np.where(k_list_length[1:]-k_list_length[:-1]>1e-4)[0]+1)+[len(k_list)]

    exclude=[]

    for start,end in zip(wall[:-1],wall[1:]):
        for l in range(start,end):
            i=k_list_sort[l]
            if new_points is not None:
                if i<n-new_points:
                   continue 
            if i not in exclude:
                for m in range(l+1,end):
                    j=k_list_sort[m]
                    if not j in exclude:
                        if k_list[i].equiv(k_list[j]):
                             exclude.append(j)
                             k_list[i].absorb(k_list[j])
    for i in sorted(exclude)[-1::-1]:
        del k_list[i]
    print ("Done. Excluded  {} points in {} sec".format(len(exclude),time()-t0))
    return cnt

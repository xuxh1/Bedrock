import xarray as xr



list_1=[1,4,5,7,3,6,7,9]
list_1=set(list_1)
print(list_1,type(list_1))
list_2=set([2,6,0,6,22,8,4])
print(list_2,type(list_2))

print("--------------------------------")
print("方法一")
print(list_1.intersection(list_2))
print("方法二")
print(list_1&list_2)
print("--------------------------------")


print("方法一")
print(list_1.union(list_2))
print("方法二")
print(list_1|list_2)
print("--------------------------------")


print(list_1.difference(list_2))
print(list_1-list_2)
print("--------------------------------")


list_3=[1,4,6]
list_4=[1,4,6,7]
list_3=set(list_3)
list_4=set(list_4)
print("方法一")
print(list_3.issubset(list_4))
print("方法二")
print(list_4.issuperset(list_3))
print("--------------------------------")


print("方法一")
print(list_1.symmetric_difference(list_2))
print("方法二")
print(list_1^list_2)
print("--------------------------------")


list_1.add('x')
print(list_1)


list_1.update([10,37,42])
print(list_1)


list_1.remove(10)
print(list_1)



print(len(list_1))



print(9 in list_1)



print(list_1.pop())



list_1.discard('x')
print(list_1)
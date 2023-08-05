# coding:utf-8

def bubbleSort(nums):
    for i in range(len(nums)-1):    # 这个循环负责设置冒泡排序进行的次数
        for j in range(len(nums)-i-1):  # ｊ为列表下标
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums
import random
import time
a=[]
for x in range(10000):
    a.append(random.randint(0,10000))
print("生成完成，共10000个随机数，最大值为10000，最小值为0，请稍后...")
tmp=time.time()
c=a[:]
y=time.time()
b=bubbleSort(c)
z=time.time()
n=z-y
print("冒泡排序用时",n,"秒")
def cocktailSort(the_list):
    the_len = len(the_list)
    if the_len <2:#0和1
        return the_list
    else:
        while 1:
            flag = False
            for i in range(the_len-1):
                if the_list[i] > the_list[i+1]:
                    the_list[i], the_list[i+1] = the_list[i+1], the_list[i]
            j = the_len-1
            while j > 0:
                if the_list[j-1] > the_list[j]:
                    the_list[j], the_list[j-1] = the_list[j-1], the_list[j]
                    flag = True
                j -= 1
            if flag == False:
                break
        return the_list
c=a[:]
y=time.time()
b=cocktailSort(c)
z=time.time()
n=z-y
print("鸡尾酒排序用时",n,"秒")
def insertSort(arr):
    length = len(arr)
    for i in range(1,length):
        x = arr[i]
        for j in range(i,-1,-1):
            # j为当前位置，试探j-1位置
            if x < arr[j-1]:
                arr[j] = arr[j-1]
            else:
                # 位置确定为j
                break
        arr[j] = x
    return arr
c=a[:]
y=time.time()
b=insertSort(c)
z=time.time()
n=z-y
print("插入排序用时",n,"秒")
def bucketSort(nums):
  # 选择一个最大的数
  max_num = max(nums)
  # 创建一个元素全是0的列表, 当做桶
  bucket = [0]*(max_num+1)
  # 把所有元素放入桶中, 即把对应元素个数加一
  for i in nums:
    bucket[i] += 1
  # 存储排序好的元素
  sort_nums = []
  # 取出桶中的元素
  for j in range(len(bucket)):
    if bucket[j] != 0:
      for y in range(bucket[j]):
        sort_nums.append(j)
  return sort_nums

c=a[:]
y=time.time()
b=bucketSort(c)
z=time.time()
n=z-y
print("桶排序用时",n,"秒")
def countSort(s):
    min_num = min(s)
    max_num = max(s)
    count_list = [0]*(max_num-min_num+1)
    for i in s:
        count_list[i-min_num] += 1
    s.clear()
    for ind,i in enumerate(count_list):
        while i != 0:
            s.append(ind+min_num)
            i -= 1
    return s
c=a[:]
y=time.time()
b=countSort(c)
z=time.time()
n=z-y
print("计数排序用时",n,"秒")
def merge(arr, l, m, r): 
    n1 = m - l + 1
    n2 = r- m 
  
    # 创建临时数组
    L = [0] * (n1)
    R = [0] * (n2)
  
    # 拷贝数据到临时数组 arrays L[] 和 R[] 
    for i in range(0 , n1): 
        L[i] = arr[l + i] 
  
    for j in range(0 , n2): 
        R[j] = arr[m + 1 + j] 
  
    # 归并临时数组到 arr[l..r] 
    i = 0     # 初始化第一个子数组的索引
    j = 0     # 初始化第二个子数组的索引
    k = l     # 初始归并子数组的索引
  
    while i < n1 and j < n2 : 
        if L[i] <= R[j]: 
            arr[k] = L[i] 
            i += 1
        else: 
            arr[k] = R[j] 
            j += 1
        k += 1
  
    # 拷贝 L[] 的保留元素
    while i < n1: 
        arr[k] = L[i] 
        i += 1
        k += 1
  
    # 拷贝 R[] 的保留元素
    while j < n2: 
        arr[k] = R[j] 
        j += 1
        k += 1
  
def mergeSort(arr,l,r): 
    if l < r: 
  
        
        m = int((l+(r-1))/2)
  
       
        mergeSort(arr, l, m) 
        mergeSort(arr, m+1, r) 
        merge(arr, l, m, r) 
c=a[:]
y=time.time()
b=mergeSort(c,0,len(c)-1)
z=time.time()
n=z-y
print("归并排序用时",n,"秒")
def radix_sort_nums(nums):
    max = nums[0]
    for i in nums:
        if max < i:
            max = i
    times = 0
    while max > 0:
        max = int(max/10)
        times += 1
    return times

# 每个数字各个位置的数字大小，比如（123,1）则是3，（123,2）则是2
def get_num(num,n):
    return (int(num/(10**(n-1)))) % 10

# 主程序
def radixSort(nums):
    count = 10*[None]	# 定义的数组，用于存放当前位数的元素个数
    bucket = len(nums)*[None]	# 用于暂时存放排序结果
	# 分别从个位/十位/百位开始循环
    for pos in range(1, radix_sort_nums(nums)+1):
		# 每次排序完都要清空各个位数存放的数据统计
        for i in range(10):
            count[i] = 0

        for i in range(len(nums)):
			# 获得0到9每个位数的个数
            j = get_num(nums[i], pos)
            count[j] = count[j]+1
		# 获得相对应位数的边界值
        for i in range(1, 10):
            count[i] = count[i] + count[i-1]

        for i in range(len(nums)-1, -1, -1):
			# 求出相应位数的数字
            j = get_num(nums[i], pos)
			#将元素按相应位数的上数字的大小排序
            bucket[count[j]-1] = nums[i]
			#让相应位数上数字相等的元素不会放在同一位置而被替代
            count[j] = count[j]-1

		# 将暂时存储在bucket的元素数据返回到nums中
        for i in range(0, len(nums)):
            nums[i] = bucket[i]
    return nums
c=a[:]
y=time.time()
b=radixSort(c)
z=time.time()
n=z-y
print("基数排序用时",n,"秒")
def gnomeSort(unsorted):
    """
    地精排序，默认升序
    算法思想：定义一个变量i,如果a[i-1]<=a[i],i=i+1,
    否则，则交换，并把i变为i-1,就这样来回移动索引位置，
    是整个列表有序
    这个排序算法是稳定的
    """


    if len(unsorted) <= 1:
        return unsorted
        
    i = 1
    
    while i < len(unsorted):
        if unsorted[i-1] <= unsorted[i]:
            i += 1
        else:
            unsorted[i-1], unsorted[i] = unsorted[i], unsorted[i-1]
            i -= 1
            if (i == 0):
                i = 1

    return unsorted
c=a[:]
y=time.time()
b=gnomeSort(c)
z=time.time()
n=z-y
print("地精排序用时",n,"秒")
print("稳定排序结束！")

print("开始不稳定排序...")
def quick_sort_num(nums,start,end):
    if start < end:
    	# 定义基准值为第一个数
        i, j, pivot = start, end, nums[start]
        while i < j:
        	# 将基准数右边的数中比基准数小的放到左边
            while i < j and nums[j] >= pivot:
                j = j-1
            if i < j:
                nums[i] = nums[j]
                i = i+1
            # 将基准数左边的数中比基准数大的数放到右边
            while i < j and nums[i] < pivot:
                i = i+1
            if i < j:
                nums[j] = nums[i]
                j = j-1
        nums[i] = pivot
        # 分别将基准数左边的数列和右边的数列进行递归
        quick_sort_num(nums, start, i-1)
        quick_sort_num(nums, i+1, end)
    return nums

# 快速排序主体函数
def quickSort(nums):
    start = 0
    end = len(nums)-1
    nums = quick_sort_num(nums, start, end)
    return nums
c=a[:]
y=time.time()
b=quickSort(c)
z=time.time()
n=z-y
print("快速排序用时",n,"秒")
def heapSort(arr):
    # 排序节点
    def node_sort(_arr, _n, _N):
        if _N < 2*_n:
            return
        elif _N == 2*_n:
            if _arr[_n] > _arr[2*_n]:
                _arr[_n], _arr[2*_n] = _arr[2*_n], _arr[_n]
        else:
            min_butree =  2*_n+1 if _arr[2*_n] > _arr[2*_n+1] else 2*_n
            if _arr[_n] > _arr[min_butree]:
                _arr[_n], _arr[min_butree] = _arr[min_butree], _arr[_n]
                node_sort(_arr, min_butree, _N)

    # 初始化得到最大堆
    N = len(arr) - 1
    for i in range(len(arr), 0, -1):
        node_sort(arr, i, N)

    # 堆顶与堆尾交换，下沉后重复得到从大到小排序
    for i in range(N-2):
        arr[1], arr[N-i] = arr[N-i], arr[1]
        node_sort(arr, 1, N-i-1)
    arr[1], arr[2] = arr[2], arr[1]
    return arr
c=a[:]
y=time.time()
b=heapSort(c)
z=time.time()
n=z-y
print("堆排序用时",n,"秒")
from itertools import zip_longest
 
def beadSort(l):
    return list(map(sum, zip_longest(*[[1] * e for e in l], fillvalue=0)))
c=a[:]
y=time.time()
b=beadSort(c)
z=time.time()
n=z-y
print("珠排序用时",n,"秒")

def shellSort(arr): 
  
    n = len(arr)
    gap = int(n/2)
  
    while gap > 0: 
  
        for i in range(gap,n): 
  
            temp = arr[i] 
            j = i 
            while  j >= gap and arr[j-gap] >temp: 
                arr[j] = arr[j-gap] 
                j -= gap 
            arr[j] = temp 
        gap = int(gap/2)
    return arr
c=a[:]
y=time.time()
b=shellSort(c)
z=time.time()
n=z-y
print("希尔排序用时",n,"秒")
cnt=time.time()
print("总共用时",cnt-tmp,"秒")

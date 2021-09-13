from youtubesearchpython import VideosSearch

search = VideosSearch("파이썬", limit=5)
resultList = []
resultdic = search.result()
for i in range(0, 5):
    resultList.append(resultdic['result'][i]['link'])
print(resultList)
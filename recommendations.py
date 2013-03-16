# A dictionary of movie critics and their ratings of a small
# set of movies
from math import sqrt

def sim_dist(prefs , person1 , person2):
  #get the listof shared items 
  si={}
  for item in prefs[person1]:
    if item in prefs[person2]:
     si[item]=1

  #when no ratings in common len(si)=0 
  if len(si) ==0: 
     return 0 
  #Adding the squares of all the differences between the two people 
  sum_of_sq=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                 for item in prefs[person1] if item in prefs[person2]])
  
  return 1./(1+sum_of_sq)

#pearson correlation coefficient similarity function 
def sim_pearson(prefs,p1,p2):
 si={} 
 for item in prefs[p1]: 
   if item in prefs[p2]: si[item]=1
 #number of items 
 n = len(si)
 
 #no ratings in common so return 0  
 if n==0:  return 0 
 #Add up all the preferences 
 sum1 = sum([prefs[p1][it] for it in si])
 sum2 =  sum([prefs[p2][it] for it in si])

 #Sum up the squares 
 sum1Sq = sum([pow(prefs[p1][it],2)for it in si])
 sum2Sq =  sum([pow(prefs[p2][it],2) for it in si])
 
 #Sum up the products 
 pSum =  sum([prefs[p1][it]*prefs[p2][it] for it in si])
 #Calculate pearson score 
 num=pSum-(sum1*sum2/n)
 den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
 if den==0: return 0
 r=num/den
 
 return r 

#function to calculate best matches for a person 
#return a list of people with their similarity scores 
def topMatches(prefs , person , n=5 ,similarity=sim_pearson):
 scores =[(similarity(prefs , person , other), other ) for other in prefs if other != person ]
 scores.sort()
 scores.reverse()
 return scores[0:n]

#Gets recommendations for a person by using a weighted average 
#of every other user's rankings 
def getRecommendations(prefs, person , similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs: 
    if other==person:
       continue 
    sim=similarity(prefs,person,other)
    print "Similarities:" , sim 
      #ignoring scores of 0 or lower 
    if sim<=0 :
        continue 
      #calculate scores (recommendations) for movies that the person has not seen yet
    for movie in prefs[other]: 
      if movie not in prefs[person] or prefs[person][movie]==0:
          #Similarity * Score 
          totals.setdefault(movie,0)
          totals[movie]+=sim*prefs[other][movie]
          #Sum of similarities 
          simSums.setdefault(movie,0)
          simSums[movie]+=sim 
          
       #normalize 
    rankings=[(total/float(simSums[movie]),movie) for movie,total in totals.items()]
  rankings.sort()
  rankings.reverse()
  return rankings


critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

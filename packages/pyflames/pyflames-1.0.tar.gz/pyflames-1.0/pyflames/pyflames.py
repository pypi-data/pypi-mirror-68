class pyflames():

    def __init__(self):
        return None
    
    def flames(self,name1,name2):
        name1 =list("".join(str(x)for x in name1.replace(" ","")))
        name2 =list("".join(str(x)for x in name2.replace(" ","")))
        common = [x for x in name1 if x in name2]
        unique = set(common)
        d=0
        for x in unique:
            d = d + min(name1.count(x),name2.count(x))
        difference = (len(name1) + len(name2)) - d*2
        target = ["Friendship","Love","Affection","Marriage","Enemity","Sibling Love"]
        while len(target)>1:
            counter = ((difference%len(target))-1)
            if counter>=0:
                part1 = target[counter+1:]
                part2 = target[:counter]
                target = part1+part2
            else:
                target = target[:len(target)-1]
        return "The relationship that exists between both of you is "+target[0]+"."
# tiny-chess-01 (MIT): compact chess engine for the make.fun gauntlet.
# Fixed node budget per move: no clock, no randomness, replay-safe.
import json,os,sys,urllib.request as U
from random import Random
E=os.environ["MAKEFUN_ENV_URL"]
def post(p,b):
 r=U.Request(E+p,data=json.dumps(b).encode(),headers={"Content-Type":"application/json"})
 return json.loads(U.urlopen(r).read())
V=[0,100,320,330,500,900,0]
KN=[];KG=[];RY=[]
for s in range(64):
 f,r=s&7,s>>3;k=[];g=[];y=[]
 for a,b in((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)):
  if 0<=f+a<8 and 0<=r+b<8:k.append(s+a+8*b)
 for a in(-1,0,1):
  for b in(-1,0,1):
   if(a or b)and 0<=f+a<8 and 0<=r+b<8:g.append(s+a+8*b)
 for a,b in((0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)):
  t=[];x,z=f,r
  while 0<=x+a<8 and 0<=z+b<8:x+=a;z+=b;t.append(x+8*z)
  y.append(t)
 KN.append(k);KG.append(g);RY.append(y)
CR=[0]*64
for s,b in((0,2),(7,1),(56,8),(63,4),(4,3),(60,12)):CR[s]=b
_R=Random(987654321)
Z={p:[_R.getrandbits(64)for _ in range(64)]for p in(-6,-5,-4,-3,-2,-1,1,2,3,4,5,6)}
ZC=[_R.getrandbits(64)for _ in range(16)];ZE=[_R.getrandbits(64)for _ in range(9)];ZS=_R.getrandbits(64)
B=[0]*64;S=1;C=0;EP=-1;HF=0;KY=0;KS=[0,0];HS=[];UN=[];HC={}
def attacked(s,by):
 f=s&7;r=s>>3
 if by>0:
  if r>0 and((f>0 and B[s-9]==1)or(f<7 and B[s-7]==1)):return 1
 elif r<7 and((f>0 and B[s+7]==-1)or(f<7 and B[s+9]==-1)):return 1
 for t in KN[s]:
  if B[t]==2*by:return 1
 for t in KG[s]:
  if B[t]==6*by:return 1
 for d in range(4):
  for t in RY[s][d]:
   p=B[t]
   if p:
    if p==4*by or p==5*by:return 1
    break
 for d in range(4,8):
  for t in RY[s][d]:
   p=B[t]
   if p:
    if p==3*by or p==5*by:return 1
    break
 return 0
def gen(cap=0):
 bd=B;mv=[];ap=mv.append
 for s in range(64):
  p=bd[s]
  if not p or(p>0)!=(S>0):continue
  t=p if p>0 else-p;f=s&7;r=s>>3
  if t==1:
   d=8*S;o=s+d;pr=r==(6 if S>0 else 1)
   if not bd[o]:
    if pr:
     for x in(5,4,3,2):ap(s|o<<6|x<<12)
    elif not cap:
     ap(s|o<<6)
     if r==(1 if S>0 else 6)and not bd[s+2*d]:ap(s|(s+2*d)<<6)
   for df in(-1,1):
    if 0<=f+df<8:
     u=o+df;q=bd[u]
     if(q and(q>0)!=(S>0))or u==EP:
      if pr:
       for x in(5,4,3,2):ap(s|u<<6|x<<12)
      else:ap(s|u<<6)
  elif t==2 or t==6:
   for u in(KN[s]if t==2 else KG[s]):
    q=bd[u]
    if not q:
     if not cap:ap(s|u<<6)
    elif(q>0)!=(S>0):ap(s|u<<6)
   if t==6:
    if S>0 and s==4:
     if C&1 and not bd[5]and not bd[6]and not attacked(4,-1)and not attacked(5,-1)and not attacked(6,-1):ap(4|6<<6)
     if C&2 and not bd[3]and not bd[2]and not bd[1]and not attacked(4,-1)and not attacked(3,-1)and not attacked(2,-1):ap(4|2<<6)
    if S<0 and s==60:
     if C&4 and not bd[61]and not bd[62]and not attacked(60,1)and not attacked(61,1)and not attacked(62,1):ap(60|62<<6)
     if C&8 and not bd[59]and not bd[58]and not bd[57]and not attacked(60,1)and not attacked(59,1)and not attacked(58,1):ap(60|58<<6)
  else:
   for d in(range(4)if t==4 else range(4,8)if t==3 else range(8)):
    for u in RY[s][d]:
     q=bd[u]
     if not q:
      if not cap:ap(s|u<<6)
     else:
      if(q>0)!=(S>0):ap(s|u<<6)
      break
 return mv
def make(m):
 global S,C,EP,HF,KY
 f=m&63;t=(m>>6)&63;pr=(m>>12)&7;p=B[f];cap=B[t];ec=0
 if p==S and t==EP and not cap and(f&7)!=(t&7):cap=-S;ec=1
 UN.append((cap,C,EP,HF,KY,ec))
 if EP>=0:KY^=ZE[EP&7]
 if cap:KY^=Z[cap][t-8*S]if ec else Z[cap][t]
 B[t]=p;B[f]=0;KY^=Z[p][f]^Z[p][t]
 if pr:
  np=pr*S;KY^=Z[p][t]^Z[np][t];B[t]=np
 if ec:B[t-8*S]=0
 if p==6*S:
  KS[0 if S<0 else 1]=t
  if t-f==2:B[f+1]=B[f+3];B[f+3]=0;KY^=Z[4*S][f+3]^Z[4*S][f+1]
  if f-t==2:B[f-1]=B[f-4];B[f-4]=0;KY^=Z[4*S][f-4]^Z[4*S][f-1]
 KY^=ZC[C];C&=~(CR[f]|CR[t]);KY^=ZC[C]
 EP=(f+t)//2 if abs(p)==1 and abs(t-f)==16 else-1
 if EP>=0:KY^=ZE[EP&7]
 HF=0 if abs(p)==1 or cap else HF+1
 KY^=ZS;S=-S;HC[KY]=HC.get(KY,0)+1;HS.append(KY)
def unmake(m):
 global S,C,EP,HF,KY
 k=HS.pop();HC[k]-=1;S=-S
 f=m&63;t=(m>>6)&63;pr=(m>>12)&7
 cap,C,EP,HF,KY,ec=UN.pop()
 p=B[t]
 if pr:p=S
 B[f]=p;B[t]=0
 if ec:B[t-8*S]=cap
 elif cap:B[t]=cap
 if p==6*S:
  KS[0 if S<0 else 1]=f
  if t-f==2:B[f+3]=B[f+1];B[f+1]=0
  if f-t==2:B[f-4]=B[f-1];B[f-1]=0
CT=[int(7-abs(7-2*(s&7))-abs(7-2*(s>>3)))for s in range(64)]
PR=[0,0,5,10,18,30,55,0]
def ev():
 s=0;nb=[0,0];ph=0
 for i,p in enumerate(B):
  if not p:continue
  t=p if p>0 else-p;g=1 if p>0 else-1;j=i if g>0 else i^56;c=CT[j]
  if t==1:v=100+PR[j>>3]
  elif t==2:v=320+7*c
  elif t==3:v=330+4*c;nb[0 if g>0 else 1]+=1
  elif t==4:v=500+2*c+(12 if(j>>3)==6 else 0)
  elif t==5:v=900+2*c
  elif t==6:v=7*c if ph<8 else-5*c+(14 if j in(2,6)else 0)
  else:v=0
  if 1<t<6:ph+=1 if t<4 else 2 if t==4 else 4
  s+=g*v
 if nb[0]==2:s+=28
 if nb[1]==2:s-=28
 return s*S
MATE=100000;INF=10**9;BUDGET=45000;ND=0;TT={};KL=[[0,0]for _ in range(200)]
class Ab(Exception):pass
def order(mv,tm,ply):
 def sc(m):
  if m==tm:return 1<<30
  c=B[(m>>6)&63]
  if c:return(1<<20)+V[-c if c<0 else c]*16-abs(B[m&63])
  if abs(B[m&63])==1 and(m>>6&63)==EP:return(1<<20)+1500
  k=KL[ply]
  if m==k[0]:return 1<<19
  if m==k[1]:return 1<<18
  return 0
 mv.sort(key=sc,reverse=True)
def qs(a,b,ply):
 global ND;ND+=1
 if ND>BUDGET:raise Ab
 if HF>=100 or HC.get(KY,0)>1:return 0
 chk=attacked(KS[0 if S<0 else 1],-S)
 if chk:best=-INF
 else:
  best=ev()
  if best>=b:return best
  if best>a:a=best
 mv=gen(0 if chk else 1);order(mv,0,min(ply,199))
 for m in mv:
  make(m)
  if attacked(KS[0 if S>0 else 1],S):unmake(m);continue
  s=-qs(-b,-a,ply+1);unmake(m)
  if s>best:best=s
  if s>a:a=s
  if a>=b:break
 return-MATE+ply if best==-INF else best
def search(d,a,b,ply):
 global ND;ND+=1
 if ND>BUDGET:raise Ab
 if ply and(HF>=100 or HC.get(KY,0)>1):return 0
 if d<=0:return qs(a,b,ply)
 e=TT.get(KY);tm=0
 if e:
  tm=e[3]
  if e[0]>=d and ply:
   if e[1]==0:return e[2]
   if e[1]==1 and e[2]>=b:return e[2]
   if e[1]==2 and e[2]<=a:return e[2]
 chk=attacked(KS[0 if S<0 else 1],-S)
 if chk:d+=1
 mv=gen();order(mv,tm,min(ply,199))
 best=-INF;bm=0;n=0;a0=a
 for m in mv:
  make(m)
  if attacked(KS[0 if S>0 else 1],S):unmake(m);continue
  n+=1;s=-search(d-1,-b,-a,ply+1);unmake(m)
  if s>best:best=s;bm=m
  if s>a:a=s
  if a>=b:
   if not B[(m>>6)&63]and not(abs(B[m&63])==1 and(m>>6&63)==EP):
    k=KL[min(ply,199)]
    if k[0]!=m:k[1]=k[0];k[0]=m
   break
 if not n:return-MATE+ply if chk else 0
 TT[KY]=(d,2 if best<=a0 else 1 if best>=b else 0,best,bm)
 return best
def root():
 global ND;ND=0
 lg=[]
 for m in gen():
  make(m)
  if not attacked(KS[0 if S>0 else 1],S):lg.append(m)
  unmake(m)
 if not lg:return None
 order(lg,0,0);best=lg[0]
 for d in range(1,100):
  try:
   a=-INF;cb=best
   for m in lg:
    make(m);s=-search(d-1,-INF,INF,1);unmake(m)
    if s>a:a=s;cb=m
   best=cb
  except Ab:break
  if ND>=BUDGET:break
 return best
def uci(m):
 f=m&63;t=(m>>6)&63;pr=(m>>12)&7
 return "abcdefgh"[f&7]+str(1+f//8)+"abcdefgh"[t&7]+str(1+t//8)+("nbrq"[pr-2]if pr else"")
def setfen(fen):
 global S,C,EP,HF,KY
 B[:]=[0]*64;pt=fen.split()
 for ri,row in enumerate(pt[0].split("/")):
  r=7-ri;f=0
  for ch in row:
   if ch.isdigit():f+=int(ch)
   else:
    p="pnbrqk".index(ch.lower())+1;B[f+8*r]=p if ch.isupper()else-p;f+=1
 S=1 if pt[1]=="w"else-1;C=0
 if"K"in pt[2]:C|=1
 if"Q"in pt[2]:C|=2
 if"k"in pt[2]:C|=4
 if"q"in pt[2]:C|=8
 EP=-1 if pt[3]=="-"else "abcdefgh".index(pt[3][0])+8*(int(pt[3][1])-1)
 HF=int(pt[4])if len(pt)>4 else 0
 KS[1]=B.index(6);KS[0]=B.index(-6);KY=0
 for i,p in enumerate(B):
  if p:KY^=Z[p][i]
 KY^=ZC[C]
 if EP>=0:KY^=ZE[EP&7]
 if S<0:KY^=ZS
 HS.clear();HC.clear();HC[KY]=1;HS.append(KY)
def play(u):
 f="abcdefgh".index(u[0])+8*(int(u[1])-1);t="abcdefgh".index(u[2])+8*(int(u[3])-1)
 pr="nbrq".index(u[4])+2 if len(u)==5 else 0
 for m in gen():
  if(m&63)==f and(m>>6&63)==t and(m>>12&7)==pr:make(m);return
 raise ValueError(u)
def main():
 while True:
  g=post("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   setfen(g["start_fen"]);TT.clear()
   for u in g["moves"]:play(u)
   try:
    m=root();mv=uci(m)if m is not None else g["legal_moves"][0]
   except Exception:mv=g["legal_moves"][0]
   if mv not in g["legal_moves"]:mv=g["legal_moves"][0]
   g=post("/move",{"game":g["game"],"move":mv})
  print("game",g["game"],g["outcome"],g["reason"],file=sys.stderr)
 print("done",file=sys.stderr)
if __name__=="__main__":main()

import os
import random
config = ['C075']
formula = 'mandelbar'
config.append(formula)
pRe = '2E+00'
config.append(pRe)
pIm = '0E+00'
config.append(pIm)
cRe = '4.076863488000000226311385631561279296879E-01'
#config.append(cRe)
cIm = '2.764800000000000000000000000000000000004E-01'
#config.append(cIm)
centerX = '%1.39E' % random.uniform(0.5335937634299654468450856981083483135243,0.5336294265408812762418861170822041397943)
config.append(centerX)
centerY = '%1.39E' % random.uniform(-1.078106126664962565088665507903649643898,-1.078058554869639261420995623222322016834)
config.append(centerY)
spanX = '%1.39E' % random.uniform(0,0.000018)
config.append(spanX)
config.append(spanX)
bailoutRadius = '1000'
config.append(bailoutRadius)
maxIterations = '1000'
config.append(maxIterations)
striptDensity = '1'
config.append(striptDensity)
spaceColor = '0x0'
config.append(spaceColor)
coloringMethod = 'iterationcount'
config.append(coloringMethod)
iterationCount = 'smooth'
config.append(iterationCount) 
transferFunction = 'log'
config.append(transferFunction)
colorScaling = '0.45'
config.append(colorScaling)
colorOffect = '0.2'
config.append(colorOffect)
# gradiernt = []
# for num in range(0,5):
#         gradiernt.append(random.random())
#         print gradiernt[num]
# for num in sorted(gradiernt):2
#         config.append(str(num))
#         config.append('0x'+str('%x' % random.randint(0,0xffffff)))
config.append('0 0x39a0 0.25 0xffffff 0.5 0xfffe43 0.75 0xbf0800 1 0x39a0')
print config
config = [line+'\n' for line in config]
with open('config.config','w') as data:
        data.writelines(config)
f=open('log.txt','a')
f.writelines(config)
os.system('fractalnow -c config.config -x 500 -y 500 -o 1')
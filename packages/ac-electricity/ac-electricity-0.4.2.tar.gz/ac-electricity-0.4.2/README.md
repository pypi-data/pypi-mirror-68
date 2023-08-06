## acelectricity module

The aim of this project is to understand the rudiments of linear AC electrical circuits and their functioning.  

### Basic electrical quantities

- Voltage (volt)
- Current (ampere)
- Impedance Z (ohm)
- Admittance Y (siemens)
- Active power P (watt)
- Reactive power Q (var)
- Apparent power S (VA)

### Electrical laws

- Kirchhoff’s current law
- Kirchhoff’s voltage law
- Ohm's law
- Impedances, admittances in series and parallel
- Voltage divider and current divider
- Millman's theorem
- Joule's first law (S=I²Z)
- Power law (S=V.I*)

### Others features

- User-defined transfer function
- Digital filter frequency response

### AC Circuit diagram 

Circuit should only contain : 
   
- independent sine voltage source  
- independent sine current source    
- resistors, inductors, capacitors

#### Example circuit  

```
                  VL
           <---------------------
                          L1
            +------+    _  _  _
      --->--| R1   |---/ \/ \/ \-----+-------+
        IL  +------+                 |       |
                                     |       |
    ^                             IR v       v IC
    |                                |       |      ^
    |                              +---+     |  C1  |
    |                              |   |   -----    |
Vin |                              |R2 |   -----    | Vout
    |                              |   |     |      |
    |                              +---+     |      |
    |                                |       | 
                                     |       |
      -------------------------------+-------+

```

Datas :  
Vin = 5 Vrms  
Inductor : L1 = 100 mH ; R1 = 180 Ω  
R2 = 2.2 kΩ ; C1 = 330 nF     

What are the IL, IR, IC currents ?  
What are the VL, Vout voltages ?  
What is the frequency response Vout/Vin ?


```python  
>>> from acelectricity import *
>>> Vin = Voltage(5)  # Vrms
>>> Zr1 = Impedance(r=180)
>>> Zl1 = Impedance(l=0.1)
>>> Zr2 = Impedance(r=2200)
>>> Zc1 = Impedance(c=330e-9)

>>> Zeq1 = 1/(1/Zr2 + 1/Zc1)  # impedances in parallel
>>> # or Zeq1 = Zr2//Zc1
>>> Zeq1
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
>>> Zeq = Zr1 + Zl1 + Zeq1  # impedances in series
>>> Zeq(2000)  # @ 2000 Hz
(206.11818300356995+1018.3560443060462j)
>>> IL = Vin/Zeq  # Ohm's law
>>> IL.properties(2000)
Frequency (Hz) : 2000
Angular frequency (rad/s) : 12566.4

Complex current : 0.000954663-0.00471665j
Amplitude (Arms) : 0.00481229
Amplitude (A) : 0.00680561
Amplitude (dBA ref 1 Arms) : -46.3529621108357
Phase (degrees) : -78.5577
Phase (radians) : -1.37109
i(t) = 0.00680561×sin(12566.4×t -1.371091)

>>> Vout = IL*Zeq1  # Ohm's law
>>> VL = Vin-Vout  # Kirchhoff’s voltage law
>>> IC = Vout/Zc1  # Ohm's law
>>> IR = IL-IC  # Kirchhoff’s current law
>>> H = Vout/Vin  # transfer function

>>> # draw Bode plot and save datas
>>> H.bode(title='Vout/Vin transfer function', filename='h.csv')
>>> IL.bode(magnitude_unit='default', yscale='linear', title='IL current')
>>> Zeq.bode(yscale='log', title='Zeq frequency response')
>>> show()
```

![screenshot1](http://fsincere.free.fr/isn/python/download/dc/image1.png)

![screenshot2](http://fsincere.free.fr/isn/python/download/dc/image2.png)

![screenshot2b](http://fsincere.free.fr/isn/python/download/dc/image2b.png)

#### Impedances and admittances

```python
>>> Yr2 = 1/Zr2
>>> Yc1 = 1/Zc1
>>> Yc1
Complex admittance (S) : 0+0.00207345j @ 1.0 kHz
>>> 1/Yc1
Complex impedance (Ω) : 0-482.288j @ 1.0 kHz
>>> 1/(Yr2+Yc1)
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
>>> Zr2*(Zc1/(Zr2+Zc1))
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
```

#### Law class

```python
>>> law = Law()
>>> # voltage divider
>>> Vout = law.VoltageDivider(vtotal=Vin, z=Zr2//Zc1, z2=Zr1+Zl1)
>>> Vout
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> Vin*(Zeq1/Zeq)
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> # Millman's theorem
>>> gnd = Voltage(0)
>>> Vout = law.Millman(v_z=[(Vin, Zr1+Zl1), (gnd, Zr2), (gnd, Zc1)])
>>> Vout
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> (Vin/(Zr1+Zl1))/(1/(Zr1+Zl1) +1/Zr2 +1/Zc1)
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> Vout/Vin
Ratio : -0.457615-1.36438j @ 1.0 kHz
>>> # current divider
>>> IC = law.CurrentDivider(itotal=IL, z=Zc1, z2=Zr2)
>>> IC
Complex current (Arms) : 0.0141449-0.00474421j @ 1.0 kHz
>>> IL*Zr2/(Zr2 +Zc1)
Complex current (Arms) : 0.0141449-0.00474421j @ 1.0 kHz
```

#### Electrical power, Joule's first law

```python
>>> S = IL*Vin  # input source complex power
>>> S.properties(1000)
Frequency (Hz) : 1000
Angular frequency (rad/s) : 6283.19

Complex power : 0.0655242+0.0392254j

Active power P (W) : +0.0655242
Reactive power Q (var) : +0.0392254
Apparent power S (VA) : 0.0763678

Phase (degrees) : +30.9064
Phase (radians) : +0.539419
Power factor PF : 0.8580073402000852

Active power (dBW ref 1 W) : -11.835985322667693

>>> Sr1 = law.Joule(z=Zr1, i=IL)
>>> Sr1
Complex power (W): 0.0419907+0j @ 1.0 kHz
>>> Zr1*IL*IL
Complex power (W): 0.0419907+0j @ 1.0 kHz
>>> Sr2 = law.Joule(z=Zr2, v=Vout)
>>> Sr2
Complex power (W): 0.0235334 @ 1.0 kHz
>>> Sl1 = Zl1*IL*IL
Complex power (W): 0+0.146575j @ 1.0 kHz
>>> Sc1 = Zc1*IC*IC
Complex power (W): 0-0.10735j @ 1.0 kHz
>>> Sr1 +Sr2 +Sc1 +Sl1
Complex power (W): 0.0655242+0.0392254j @ 1.0 kHz
```

#### Parameters analysis

```python  
>>> Vin.RMS = 10
>>> Vin.phase = 45
>>> Zr1.r = 100
>>> Zl1.l = 0.22
>>> Zr2.r = 1000
>>> Zc1.c = 100e-9
>>> H.bode(title='Vout/Vin transfer function', filename='h2.csv')
>>> IL.bode(magnitude_unit='default', yscale='linear', title='IL current')
>>> Zeq.bode(yscale='log', title='Zeq frequency response')
>>> show()
```

![screenshot2c](http://fsincere.free.fr/isn/python/download/dc/image2c.png)

![screenshot2d](http://fsincere.free.fr/isn/python/download/dc/image2d.png)

![screenshot2e](http://fsincere.free.fr/isn/python/download/dc/image2e.png)


```python  
>>> for Zr2.r in [10, 100, 1e3, 1e4]:
        H.bode(title="Vout/Vin with R2={} Ω".format(Zr2.r))
>>> show()
```

### User-defined transfer function

#### Example 1 : second order band-pass filter

```python
>>> from acelectricity import *
>>> # static gain, damping value, normal angular frequency
>>> a, z, wn = 10, 0.1, 1000*2*math.pi
>>> H = Ratio(fw=lambda w: a*(2*z*1j*w/wn)/(1+2*z*1j*w/wn-(w/wn)**2))
>>> H.bode(filename='H.csv')
>>> a, z, wn = 100, 0.5, 10000
>>> H.bode(filename='H2.csv')
>>> show()
```

or :  

```python
>>> a, z, wn = 10, 0.1, 1000*2*math.pi
>>> H = Ratio.transfer_function(numerator=[0, a*(2*z*1j/wn)],
    denominator=[1, 2*z*1j/wn, -1/wn**2])
>>> H.bode(filename='H3.csv')
>>> a, z, wn = 100, 0.5, 10000
>>> # new instance
>>> H = Ratio.transfer_function(numerator=[0, a*(2*z*1j/wn)],
    denominator=[1, 2*z*1j/wn, -1/wn**2])
>>> H.bode(filename='H4.csv')
>>> show()
```


 
#### Example 2 : cascaded series, parallel filters

```python
>>> from acelectricity import *
>>> # first order low-pass filter
>>> wn = 10000
>>> Hlp = Ratio(fw=lambda w: 1/(1+1j*w/wn))
>>> # first order high-pass filter
>>> Hhp = Ratio(fw=lambda w: 1/(1+1j*wn/w))
>>> Hs = Hlp*Hhp  # cascaded series filters
>>> Hs.bode()
>>> Hp = Hlp+Hhp  # parallel filters
>>> Hp.bode()
>>> show()
```

#### Example 3 : linear control system

```
          +      +------+
     -->---(X)---| G(w) |----+--->--
          - |    +------+    |
            |                |
            |    +------+    |
            +----| H(w) |-<--+
                 +------+

```

```python
>>> from acelectricity import *
>>> # feedforward transfer function
>>> # first order low-pass filter
>>> wn = 10000
>>> G = Ratio.transfer_function([1], [1, 1j/wn])
>>> # feedback transfer function
>>> H = Ratio.transfer_function([10])  # constant
>>> # open-loop transfer function
>>> Hopenloop = G*H
>>> Hopenloop.bode()
>>> # closed-loop transfer function
>>> Hcloseloop = G/(1+Hopenloop)
>>> Hcloseloop.bode()
>>> show()
```

### Digital filter frequency response

```
y(n) = 0.1x(n) +1.6y(n-1) -0.7y(n-2)
```

```python
>>> from acelectricity import *
>>> fs = 100000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[0.1], a=[1, -1.6, 0.7])
>>> H.bode(xmin=fs*0.001, xmax=fs/2, xscale='linear',
    title='IIR digital filter')
>>> show()
```

![screenshot3](http://fsincere.free.fr/isn/python/download/dc/image3.png)

```
y(n) = (x(n)+x(n-1)+x(n-2)+x(n-3))/4
```

```python
>>> from acelectricity import *
>>> fs = 10000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[0.25]*4)
>>> H.bode(xmin=fs*0.001, xmax=fs/2, xscale='linear',
    title='FIR digital filter')
>>> show()
```

![screenshot4](http://fsincere.free.fr/isn/python/download/dc/image4.png)


### Custom default frequency

```python
>>> from acelectricity import *
>>> Yc = Admittance(c=220e-6)
>>> Yc
Complex admittance (S) : 0+1.3823j @ 1.0 kHz
>>> ElectricalQuantity.DEFAULT_FREQUENCY = 50
>>> Yc
Complex admittance (S) : 0+0.069115j @ 50 Hz
>>> 1/Yc
Complex impedance (Ω) : 0-14.4686j @ 50 Hz
```

### Advantages and limitations

This module manages basic arithmetic operations ```+ - * /``` as well as ```//``` which designates two impedances in parallel.  

The dimensional homogeneity is checked :  

```python
>>> V3 = V1 - V2 + I3  # V+A -> Error
TypeError : Voltage expected
>>> I1 = Current(2)
>>> I = I1 + 0.5  # A+number -> Error
TypeError : Current expected
>>> I2 = Current(0.5, phase=30)
>>> I = I1 + I2
>>> I
Complex current (Arms) : 2.43301+0.25j @ 1.0 kHz
>>> I = 5*I2 - V1/Z1 + I3
```

The result of any operation must give a quantity whose unit is one of : V, A, Ω, S, W (or ratio).  
Otherwise, you will get an error :   

```python
>>> Z1/V1  # Ω/V -> 1/A -> Error
TypeError
>>> U2*(Z3/(Z2+Z3))  # V*(Ω/Ω) -> V*() -> V
>>> U2*Z3/(Z2+Z3)  # V*Ω -> Error
TypeError
>>> S = V1*(V1/Z1)  # V*(V/Ω) -> V*A -> W
>>> S = V1*V1/Z1    # V*V -> Error
TypeError
```

### See also  

[https://pypi.org/project/dc-electricity](https://pypi.org/project/dc-electricity)

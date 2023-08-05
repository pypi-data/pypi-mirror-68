![Pypi](https://img.shields.io/pypi/v/pepephone-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# pepephone-data
English Below

## Castellano
`pepephone-data` es una manera rápida para ver el uso de datos si usas Pepephone: sin tener que hacer login en la Web / aplicación móvil desde la línea de comandos.

Se necesita crear un fichero en uno de los sitios:
```
$HOME/.pepephone
/etc/pepephone
```

Con este contenido:

```
[authentication]
email = email_used_to_authenticate_on_pepephone.com
password = password_for_your_pepephone_account
phone = your_pepephone_phone_number

[extra]
extra_GB = 25
```

El estra es opcional: en este caso añade 25 GB a los datos disponibles de Pepephone. La razón: si planeas añadir datos pero no lo has hecho aún.

Ejemplo:
```
Time         : 2020-05-10 16:37:02
GB total     : 75.58 GB (Including extra 25 GB)

GB used total: 17.93 GB (EU roaming: 0.00 GB)
GB used/day  : 1.79 GB/day

GB remaining : 57.65 GB
GB remain/day: 2.62 GB/day

% Used       : 23.72%
% Month      : 32.26%
```
El `GB total` incluye los datos acumulados del mes pasados, regalos de Pepephone, etc.

## English
`pepephone-data` is a quick way to check usage data of Pepephone: without Web or mobile application from the command line.

Create a file in one of the places:
```
$HOME/.pepephone
/etc/pepephone
```

With this contents:
```
[authentication]
email = email_used_to_authenticate_on_pepephone.com
password = password_for_your_pepephone_account
phone = your_pepephone_phone_number

[extra]
extra_GB = 25
```
The extra is optional: in this case it will add 25 GB to the data available on Pepephone. The reason: you might plan to add 25 GB during the month but not have done it yet.

Execute `show-data-used.py`:
```
Time         : 2020-05-10 16:37:02
GB total     : 75.58 GB (Including extra 25 GB)

GB used total: 17.93 GB (EU roaming: 0.00 GB)
GB used/day  : 1.79 GB/day

GB remaining : 57.65 GB
GB remain/day: 2.62 GB/day

% Used       : 23.72%
% Month      : 32.26%
```

The GB total includes last months remaining data, Pepephone "gifts", etc.

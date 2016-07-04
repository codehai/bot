echo abcdefgh1234567abcZXCVBNMdefg | sed -s 's/^.*[^0-9]\([0-9]\+\).*[^A-Z]\([A-Z]\+\).*$/number:\1\nCAPITAL:\2/'

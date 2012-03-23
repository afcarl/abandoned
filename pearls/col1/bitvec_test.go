package bitvec

import (
    "testing"
)

type expect struct {
    in, out uint
    err *OutOfRangeError
}

func TestCreateBitVector(t *testing.T) {
    tests := []expect {
        expect{0, 1, nil},
        expect{127, 2, nil},
        expect{128, 3, nil},
    }
    
    for _, test := range tests {
        v := CreateBitVector(test.in)
        if len(v) != int(test.out) {
            t.Errorf("Expected width %d, got width %d\n", test.out, len(v))
        }
    }
}

func TestGetBit(t *testing.T) {
    // 11297 = 0010 1100 0010 0001
    //  7216 = 0001 1100 0011 0000
    v := BitVector([]uint64{ 11297, 7216 })
    tests := []expect {
        expect{0, 1, nil},
        expect{10, 1, nil},
        expect{63, 0, nil},
        expect{68, 1, nil},
        expect{80, 0, nil},
    }

    failTests := []expect {
        expect{128, 0, &OutOfRangeError{128}},
        expect{243, 0, &OutOfRangeError{243}},
    }

    for _, test := range tests {
        if val, err := v.GetBit(test.in); val != test.out || err != nil {
            t.Errorf("Expected %d in bit %d; got %d\n", test.out, test.in, val)
        }
    }

    for _, test := range failTests {
        val, err := v.GetBit(test.in)
        if val != 0 || err.(*OutOfRangeError).bit != test.err.bit {
            t.Errorf("Expected %d, %d on input %d; got %d, %d\n",
                test.out,
                test.err.bit,
                test.in,
                val,
                err.(*OutOfRangeError).bit)
        }
    }
}

func TestSetBit(t *testing.T) {
    v := CreateBitVector(300)
    v.SetBit(37)
    v.SetBit(128)
    v.SetBit(247)

    tests := []expect {
        expect{37, 1, nil},
        expect{128, 1, nil},
        expect{247, 1, nil},
        expect{0, 0, nil},
        expect{60, 0, nil},
        expect{139, 0, nil},
    }

    failTests := []expect {
        expect{419, 0, &OutOfRangeError{419}},
    }

    for _, test := range failTests {
        err := v.SetBit(test.in)
        if err == nil || err.(*OutOfRangeError).bit != test.err.bit {
            t.Errorf("Expected \"%s\" on input %d; got \"%s\"",
                test.err,
                test.in,
                err)
        }
    }

    for _, test := range tests {
        if val, err := v.GetBit(test.in); val != test.out || err != nil {
            t.Errorf("Expected %d in bit %d; got %d\n", test.out, test.in, val)
        }
    }
}

func TestUnsetBit(t *testing.T) {
    // 11297 = 0010 1100 0010 0001
    //  7216 = 0001 1100 0011 0000
    v := BitVector([]uint64{ 11297, 7216 })
    v.UnsetBit(68)
    v.UnsetBit(0)

    tests := []expect {
        expect{0, 0, nil},
        expect{10, 1, nil},
        expect{63, 0, nil},
        expect{68, 0, nil},
        expect{80, 0, nil},
    }

    failTests := []expect {
        expect{419, 0, &OutOfRangeError{419}},
    }

    for _, test := range failTests {
        err := v.UnsetBit(test.in)
        if err == nil || err.(*OutOfRangeError).bit != test.err.bit {
            t.Errorf("Expected \"%s\" on input %d; got \"%s\"",
                test.err,
                test.in,
                err)
        }
    }

    for _, test := range tests {
        if val, err := v.GetBit(test.in); val != test.out || err != nil {
            t.Errorf("Expected %d in bit %d; got %d\n", test.out, test.in, val)
        }
    }
}

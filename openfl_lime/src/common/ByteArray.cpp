#include <Utils.h>
#include <ByteArray.h>

namespace lime{

ByteArray::ByteArray(int Size){
    mValue = (struct _value*)malloc(Size);
    size = Size;
}

ByteArray::ByteArray(const ByteArray &inRHS){
    mValue = (struct _value*)malloc(inRHS.size);
    memcpy(mValue, inRHS.mValue, inRHS.size);
    size = inRHS.size;
}

ByteArray::ByteArray(){
    mValue = NULL;
    size = 0;
}

ByteArray::ByteArray(const QuickVec<unsigned char>  &inValue){
    int i;
    unsigned char *val = (unsigned char*)malloc(inValue.size());
    for(i = 0; i < inValue.size(); i++)
        val[i] = inValue[i];
    mValue = (struct _value*)val;
    size = inValue.size();
}

int ByteArray::Size() const{
    return size;
}

unsigned char *ByteArray::Bytes(){
    return (unsigned char*)mValue;
};

const unsigned char *ByteArray::Bytes() const{
    return (unsigned char*)mValue;
};

}
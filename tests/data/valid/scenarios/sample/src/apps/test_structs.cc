/**
 * \file
 * \brief Some basic struct unit tests.
 */

#include "generated/structs/Test1.h"
#include "generated/structs/Test2.h"
#include "generated/structs/Test3.h"
#include <cassert>
#include <cstring>
#include <iostream>

void test1_encode_decode(std::endian endianness)
{
    using namespace A::B;

    C::Test1 src;
    src.field1 = 0x55;
    src.field2 = Enum1::C;
    src.field3 = 2.5f;

    C::Test1::Buffer buffer;
    assert(src.encode(&buffer, endianness) == C::Test1::size);

    C::Test1 dst;
    assert(dst.decode(&buffer, endianness) == C::Test1::size);

    /* Verify the values transferred. */
    assert(dst.field1 == 0x55);
    assert(dst.field2 == Enum1::C);
    // assert(dst.field3 == 2.5f);
}

void test2_encode_decode(std::endian endianness)
{
    using namespace A::B;

    Test2 src;
    src.field1 = 0x55;
    src.field2 = -500;
    src.field3 = 2.5f;

    Test2::Buffer buffer;
    assert(src.encode(&buffer, endianness) == Test2::size);

    Test2 dst;
    assert(dst.decode(&buffer, endianness) == Test2::size);

    /* Verify the values transferred. */
    assert(dst.field1 == 0x55);
    assert(dst.field2 == -500);
    // assert(dst.field3 == 2.5f);
}

void test3_encode_decode(std::endian endianness)
{
    using namespace A::B;

    Test3 src = {};
    src.field1 = 70000;

    src.field2.field1 = 200;
    src.field2.field2 = Enum1::B;
    src.field2.field3 = -4000.0;

    src.field3.field1 = -100;
    src.field3.field2 = -300;
    src.field3.field3 = -5.0f;

    src.field4 = C::Enum2::green;

    Test3::Buffer buffer = {};
    assert(src.encode(&buffer, endianness) == Test3::size);

    Test3 dst = {};
    assert(dst.decode(&buffer, endianness) == Test3::size);
    assert(dst.field1 == 70000);

    assert(dst.field2.field1 == 200);
    assert(dst.field2.field2 == Enum1::B);
    // assert(dst.field2.field3 == -4000.0);
}

/**
 * A unit test for structs Test1.
 *
 * \return 0 on success.
 */
int main(void)
{
    test1_encode_decode(std::endian::native);
    test1_encode_decode(std::endian::little);
    test1_encode_decode(std::endian::big);

    test2_encode_decode(std::endian::native);
    test2_encode_decode(std::endian::little);
    test2_encode_decode(std::endian::big);

    test3_encode_decode(std::endian::native);
    test3_encode_decode(std::endian::little);
    test3_encode_decode(std::endian::big);

    std::cout << "Success." << std::endl;
    return 0;
}

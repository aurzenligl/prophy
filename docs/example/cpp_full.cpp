#include <stdio.h>
#include <iostream>
#include "values.ppf.hpp"

void print_bytes(const void* opaque_data, size_t size)
{
    const uint8_t* data = static_cast<const uint8_t*>(opaque_data);
    for (int i = 0; i < size; i++)
    {
        if (i && (i % 4 == 0))
        {
            printf("\n");
        }
        printf("%02x", data[i]);
    }
    printf("\n");
}

using namespace prophy::generated;

int main()
{
    Values msg;
    msg.transaction_id = 1234;
    msg.objects.emplace_back();
    msg.objects.emplace_back(Object{{Token::discriminator_keys_t, {1, 2, 3}}, {1, 2, 3, 4, 5}, {'\x0e'}});

    std::vector<uint8_t> data = msg.encode();
    print_bytes(data.data(), data.size());

    Values msg2;
    msg2.decode(data);
    std::cout << msg2.print();
    return 0;
}

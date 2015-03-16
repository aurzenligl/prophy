#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "values.pp.hpp"

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

void print_values(Values* x, int index)
{
    Object* obj = x->objects;
    while(index)
    {
        Object::part2* obj_part2 = prophy::cast<Object::part2*>(
                obj->values + obj->num_of_values);
        obj = prophy::cast<Object*>(
                obj_part2->updated_values +
                obj_part2->num_of_updated_values);
        --index;
    }
    printf("number of values: %d\n", obj->num_of_values);
    for (int i = 0; i < obj->num_of_values; i++)
    {
        printf("value: %d\n", obj->values[i]);
    }
}

int main()
{
    void* data = malloc(1024);
    memset(data, 0, 1024);

    Values* x = static_cast<Values*>(data);
    x->transaction_id = 1234;
    x->num_of_objects = 2;

    Object* obj = x->objects;
    obj->token.discriminator = Token::discriminator_id;
    obj->token.id = 0;
    obj->num_of_values = 0;
    Object::part2* obj_part2 = prophy::cast<Object::part2*>(obj->values);
    obj_part2->num_of_updated_values = 0;

    obj = prophy::cast<Object*>(obj_part2->updated_values);
    obj->token.discriminator = Token::discriminator_keys;
    obj->token.keys.key_a = 1;
    obj->token.keys.key_b = 2;
    obj->token.keys.key_c = 3;
    obj->num_of_values = 5;
    obj->values[0] = 1;
    obj->values[1] = 2;
    obj->values[2] = 3;
    obj->values[3] = 4;
    obj->values[4] = 5;
    obj_part2 = prophy::cast<Object::part2*>(obj->values + 5);
    obj_part2->num_of_updated_values = 1;
    obj_part2->updated_values[0] = 0x0e;

    size_t byte_size =
        reinterpret_cast<uint8_t*>(prophy::cast<Values*>(obj_part2->updated_values + 1)) -
        reinterpret_cast<uint8_t*>(x);

    printf("byte size: %d\n", byte_size);
    print_bytes(x, byte_size);
    print_values(x, 0);
    print_values(x, 1);

    return 0;
}

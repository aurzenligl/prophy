#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/printer.hpp>
#include "Arrays.ppf.hpp"
#include "util.hpp"

namespace prophy
{
namespace generated
{
struct Nestcomp : public prophy::detail::message<Nestcomp>
{
    enum { encoded_byte_size = 16 };

    Fixcomp a;
    Fixcomp b;

    Nestcomp() { }
    Nestcomp(const Fixcomp& _1, const Fixcomp& _2): a(_1), b(_2) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};
}
namespace detail
{
template <>
void message_impl<generated::Nestcomp>::print(const generated::Nestcomp& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "a", x.a);
    do_print(out, indent, "b", x.b);
}
template void message_impl<generated::Nestcomp>::print(const generated::Nestcomp& x, std::ostream& out, size_t indent);
}
}

using namespace testing;
using namespace prophy::generated;

TEST(printing, test_nested_printing)
{
    Nestcomp x{{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}};

    EXPECT_EQ(std::string(
            "a {\n"
            "  x {\n"
            "    x: 1\n"
            "    y: 2\n"
            "  }\n"
            "  y {\n"
            "    x: 3\n"
            "    y: 4\n"
            "  }\n"
            "}\n"
            "b {\n"
            "  x {\n"
            "    x: 5\n"
            "    y: 6\n"
            "  }\n"
            "  y {\n"
            "    x: 7\n"
            "    y: 8\n"
            "  }\n"
            "}\n"), x.print());
}

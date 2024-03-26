ostream& operator<<(ostream& os, const check_box& c)
{
  os << (c.on? "on " : "off ");
  return os;
}

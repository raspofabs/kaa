ostream& operator<<(ostream& os, const check_box& c)
{
  os << (c.on? "on " : "off ");
  return os;
}

ostream& operator <<(ostream& os, const my_type2& c)
{
  os << (c.on? "on " : "off ");
  return os;
}

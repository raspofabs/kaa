// taken from Emily Bache's git-repo, annotated by me
// https://github.com/emilybache/GildedRose-Refactoring-Kata/blob/main/cpp/src/GildedRose.cc
#include "GildedRose.h"

//GildedRose::GildedRose(vector<Item> & items) : items(items)
//{}
    
void GildedRose::updateQuality() 
{
    // 1 + 0 + 0 + 0 + b(510) == 511
    for (int i = 0; i < items.size(); i++)
    // body = if(15) * if(2) * if(17) = 510
    {
        // if = e(1) + c(3) + a(11) = 15
        if (items[i].name != "Aged Brie" && items[i].name != "Backstage passes to a TAFKAL80ETC concert")
        // consequence = 3
        {
            // if = 3
            if (items[i].quality > 0) 
            // consequence = 2
            {
                // if = 2
                if (items[i].name != "Sulfuras, Hand of Ragnaros")
                // consequence = 1
                {
                    items[i].quality = items[i].quality - 1;
                }
            }
        }
        // alternative = 11
        else
        {
            // if = 11
            if (items[i].quality < 50)
            {
                items[i].quality = items[i].quality + 1;

                // if = 10
                if (items[i].name == "Backstage passes to a TAFKAL80ETC concert")
                // consequence = 9
                {
                    // if = 3
                    if (items[i].sellIn < 11)
                    // consequence = 2
                    {
                        // if = 2
                        if (items[i].quality < 50)
                        // consequence = 1
                        {
                            items[i].quality = items[i].quality + 1;
                        }
                    }

                    // if = 3
                    if (items[i].sellIn < 6)
                    // consequence = 2
                    {
                        // if = 2
                        if (items[i].quality < 50)
                        // consequence = 1
                        {
                            items[i].quality = items[i].quality + 1;
                        }
                    }
                }
            }
        }

        // if = 2
        if (items[i].name != "Sulfuras, Hand of Ragnaros")
        // consequence = 1
        {
            items[i].sellIn = items[i].sellIn - 1;
        }

        // if = 7
        if (items[i].sellIn < 0)
        {
            // if = 6
            if (items[i].name != "Aged Brie")
            {
                // if = 4
                if (items[i].name != "Backstage passes to a TAFKAL80ETC concert")
                // consequence = 3
                {
                    // if = 3
                    if (items[i].quality > 0)
                    // consequence = 2
                    {
                        // if = 2
                        if (items[i].name != "Sulfuras, Hand of Ragnaros")
                        // consequence = 1
                        {
                            items[i].quality = items[i].quality - 1;
                        }
                    }
                }
                else
                // alternative = 1
                {
                    items[i].quality = items[i].quality - items[i].quality;
                }
            }
            else
            // alternative = 2
            {
                // if = 2
                if (items[i].quality < 50)
                // consequence = 1
                {
                    items[i].quality = items[i].quality + 1;
                }
            }
        }
    }
}

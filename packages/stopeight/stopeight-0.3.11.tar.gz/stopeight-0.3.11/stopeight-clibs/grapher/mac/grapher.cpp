/*
 *  grapher.cpp
 *  grapher
 *
 *  Created by Fassio Blatter on 13/07/2017.
 *  Copyright © 2017 Fassio Blatter. All rights reserved.
 *
 */

#include <iostream>
#include "grapher.hpp"
#include "grapherPriv.hpp"

void grapher::HelloWorld(const char * s)
{
    grapherPriv *theObj = new grapherPriv;
    theObj->HelloWorldPriv(s);
    delete theObj;
};

void grapherPriv::HelloWorldPriv(const char * s) 
{
    std::cout << s << std::endl;
};


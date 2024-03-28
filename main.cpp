//
// Created by Nicolas Buchwalder on 27.03.24.
//

#include "Organism.h"
#include "Environment.h"


int main1() {
    Environment<100, 100> environment;
    environment.generate<Organism<2, 2>>(5);
    return 0;
}
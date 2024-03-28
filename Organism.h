//
// Created by Nicolas Buchwalder on 27.03.24.
//

#ifndef NEURALNET_EVOLUTION_ORGANISM_H
#define NEURALNET_EVOLUTION_ORGANISM_H

#include "Entity.h"
#include "Gene.h"

#include <array>

template <int I, int O>
class Organism : public Entity {
private:
    Gene<I, O> genome;

public:
    Organism() {
        genome = Gene<I, O>(0.1);
    };

    Organism(Organism<I, O>& parent) {
        genome = Gene<I, O>(parent);
    };

    Organism(Organism<I, O>& parent1, Organism<I, O>& parent2) {
        genome = Gene<I, O>(parent1, parent2);
    };

    std::array<float, O> react(std::array<float, I> sensors) {
        return genome.think(sensors);
    };
};


#endif //NEURALNET_EVOLUTION_ORGANISM_H

//
// Created by Nicolas Buchwalder on 27.03.24.
//

#ifndef NEURALNET_EVOLUTION_GENE_H
#define NEURALNET_EVOLUTION_GENE_H

#include <array>
#include <random>

template <int I, int O>
class Gene {
private:
   float mutationRate;
    std::array<std::array<float, I>, O> genome;

    static std::mt19937& get_generator() {
        static std::random_device rd;
        static std::mt19937 gen(rd());
        return gen;
    }

    static std::normal_distribution<float>& get_distribution() {
        static std::normal_distribution<float> dist(0.0, 1.0);
        return dist;
    }

public:
    Gene() = default;

    explicit Gene(float _mutationRate) : mutationRate(_mutationRate) {
        auto& gen = get_generator();
        auto& dist = get_distribution();

        for (int i = 0; i < O; i++) {
            for (int j = 0; j < I; j++) {
                genome[i][j] = dist(gen);
            }
        }
    }

    Gene(Gene& parent) : mutationRate(parent.mutationRate), genome(parent.genome) {
        mutate();
    };

    Gene(Gene& parent1, Gene& parent2) {
        mutationRate = (parent1.mutationRate + parent2.mutationRate) / 2.0;

        auto& gen = get_generator();
        auto& dist = get_distribution();

        for (int i = 0; i < O; i++) {
            for (int j = 0; j < I; j++) {
                genome[i][j] = (parent1.genome[i][j] + parent2.genome[i][j]) / 2.0;
            }
        }
        mutate();
    }

    void mutate() {
        int numGenesToMutate = static_cast<int>(mutationRate * I * O);
        auto& gen = get_generator();
        auto& dist = get_distribution();

        for (int i = 0; i < numGenesToMutate; i++) {
            int randomIndexI = gen() % I;
            int randomIndexO = gen() % O;
            genome[randomIndexO][randomIndexI] = dist(gen);
        }
    }

    std::array<float, O> think(std::array<float, I> sensors) {
        std::array<float, O> actions;
        for (int i = 0; i < O; i++) {
            actions[i] = 0;
            for (int j = 0; j < I; j++) {
                actions[i] += genome[i][j] * sensors[j];
            }
        }
        return actions;
    }


};



#endif //NEURALNET_EVOLUTION_GENE_H

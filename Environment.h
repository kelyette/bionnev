//
// Created by Nicolas Buchwalder on 27.03.24.
//

#ifndef NEURALNET_EVOLUTION_ENVIRONMENT_H
#define NEURALNET_EVOLUTION_ENVIRONMENT_H

#include "Entity.h"

#include <array>
#include <list>
#include <random>
#include <memory>
#include <iostream>

template<int W, int H>
class Environment {

private:
    std::array<std::array<std::list<std::unique_ptr<Entity>>, W>, H> entities;
    std::random_device rd;
    std::mt19937 gen;
    std::uniform_int_distribution<> distribX{0, W-1};
    std::uniform_int_distribution<> distribY{0, H-1};

public:
    Environment() = default;

    template <class T>
    void generate(int N) {
        for (int i = 0; i < N; i++) {
            addEntity(std::make_unique<T>(), distribX(gen), distribY(gen));
        }
    }

    void moveEntity(int id, int currentX, int currentY, int moveX, int moveY) {
        auto &currentList = entities[currentX][currentY];
        for (auto iter = currentList.begin(); iter != currentList.end(); ++iter) {
            if ((*iter)->getId() == id) { // Assuming Entity has a getId() method for simplicity
                int newX = std::min(std::max(currentX + moveX, 0), W - 1);
                int newY = std::min(std::max(currentY + moveY, 0), H - 1);

                // Transfer ownership and remove from current list
                auto entity = std::move(*iter);
                currentList.erase(iter);

                // Add to the new position's list
                entities[newX][newY].push_back(std::move(entity));

                std::cout << "Moved entity " << id << " to " << newX << ", " << newY << std::endl;
                break; // Exit the loop once the entity is found and moved
            }
        }
    }


private:

    void addEntity(std::unique_ptr<Entity> entity, int x, int y){
        std::cout << "Adding entity at " << x << ", " << y << std::endl;
        entities[x][y].push_back(std::move(entity));
    }
    std::list<std::unique_ptr<Entity>> getEntities(int x, int y){
        return entities[x][y];
    }
};


#endif //NEURALNET_EVOLUTION_ENVIRONMENT_H

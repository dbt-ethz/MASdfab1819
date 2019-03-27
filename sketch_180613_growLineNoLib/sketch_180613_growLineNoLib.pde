/*
Line Growth History by Patrick Bedarf
www.bedarf.cc

Inspired by
https://github.com/shiffman/The-Nature-of-Code-Examples
https://n-e-r-v-o-u-s.com/projects/sets/puzzles/
https://inconvergent.net/2016/shepherding-random-growth/
and your garden lettuce
*/

Chain chain;
boolean pause;
int growTimer;

void setup() {
	size(580, 580);
	growTimer = 0;
	init();
}

void draw() {
	//background(240);
	smooth();
	chain.run();

	//text("Nodes " + chain.nodes.size(), 30, 30);
	//text("Links " + chain.links.size(), 30, 50);
	//text("Timer " + (int)chain.growTimer, 30, 70);
}

void init() {
	background(240);
	chain = new Chain(40, 100, 800, 50);
}

void keyPressed() {
	if (key == 'r') {
		init();
	}
    else if ((key == 'p') && (pause == false)) {
        pause = true;
        noLoop();
    }
    else if ((key == 'p') && (pause == true)) {
        pause = false;
        loop();
    }
}

class Chain {
	ArrayList<Node> nodes = new ArrayList<Node>();
	ArrayList<Link> links = new ArrayList<Link>();
	int numPoints;
    float attStrength, repStrength, repRadius, radius, angle, len, splitValue, interval;

    // Chain constructor
    Chain(int _numPoints, float _radius, float _attStrength, float _repStrength) {

      numPoints = _numPoints;
      radius = _radius;
      attStrength = _attStrength;
      repStrength = _repStrength;

      angle = TWO_PI/(float)numPoints;
      len = TWO_PI * radius / numPoints;

      repRadius = len;		// set this parameter to control initial growth
      splitValue = len;		// set this parameter to control growth density
	  interval = 0.5;			// set this parameter to control growth speed

	  // initialize nodes
	  for (int i = 0; i < numPoints; i++) {
		  Node node = new Node(radius*sin(angle*i)+width/2, radius*cos(angle*i)+height/2);
		  nodes.add(node);
	  }
  }

	  void run() {
		  updateNodes();
		  updateLinks();
		  growth_1(interval);
	  }

	  void growth_1(float t) {
		  growTimer += 1;
		  if (growTimer > 30*t) {
			  int i = (int)random(links.size());
			  if (links.get(i).distance > splitValue) {
				  links.get(i).splitLink(splitValue);
				  growTimer = 0;
			  }
		  }
	  }

	  void updateNodes() {
		  for (int i = 0; i < nodes.size(); i++) {
				nodes.get(i).update(i, repRadius, repStrength);
    		}
	  }

	  void updateLinks() {
		  links.clear();
		  for (int i = 0; i < nodes.size(); i++) {
			  if (i < nodes.size()-1) {
				  Link link = new Link(i, i+1, attStrength, repRadius);
				  links.add(link);
			  } else {
				  Link link = new Link(i, 0, attStrength, repRadius);
				  links.add(link);
			  }
		  }
		  for (Link link : links) {
			  link.update();
		  }
	  }
  }

class Link {
	float length, distance, attStrength, repRadius;
	int i1, i2;

	Link(int _i1, int _i2, float _attStrength, float _repRadius) {
		i1 = _i1;
		i2 = _i2;
		attStrength = _attStrength;
		repRadius = _repRadius;
		distance = PVector.sub(chain.nodes.get(i1).location, chain.nodes.get(i2).location).mag();
	}

	void update() {
		if (growTimer < 1) {
			display();
		}
		applyAttraction();
	}

	void display() {
		float c = 200 - (chain.nodes.size() - chain.numPoints);
		stroke(constrain(c, 0, 255));
		strokeWeight(0.5);
		line(chain.nodes.get(i1).location.x, chain.nodes.get(i1).location.y, chain.nodes.get(i2).location.x, chain.nodes.get(i2).location.y);
		}

	void applyAttraction() {
		if (repRadius < PVector.sub(chain.nodes.get(i1).location, chain.nodes.get(i2).location).mag()) {
			PVector force1 = chain.nodes.get(i1).attract(chain.nodes.get(i2), attStrength);
			PVector force2 = chain.nodes.get(i2).attract(chain.nodes.get(i1), attStrength);
			force1.mult(0.5);
			force2.mult(0.5);
			chain.nodes.get(i1).applyForce(force1);
			chain.nodes.get(i2).applyForce(force2);
		}
	}

	void splitLink(float splitValue) {
		if (distance > splitValue) {
			float newX = (chain.nodes.get(i1).location.x + chain.nodes.get(i2).location.x) / 2;
			float newY = (chain.nodes.get(i1).location.y + chain.nodes.get(i2).location.y) / 2;
			Node newNode = new Node(newX, newY);
			chain.nodes.add(i2, newNode);
		}
	}
}


class Node {
	PVector location, velocity, acceleration, friction;
	float topspeed, G;

	Node(float x, float y) {
		location = new PVector(x, y);
		velocity = new PVector(0, 0);
		acceleration = new PVector(0, 0);
		friction = new PVector(0, 0);
		topspeed = 0.5;
		G = -0.4;
	}

	void update(int i, float repRadius, float repStrength) {
		velocity.add(acceleration);
		velocity.limit(topspeed);
		location.add(velocity);
		acceleration.mult(0);
		applyFriction();
		applyRepulsion(i, repRadius, repStrength);
		boundaries();
		//display();
	}

	void display() {
		noStroke();
		fill(80);
		ellipse(location.x, location.y, 10, 10);
	}

	void applyFriction() {
		PVector force = velocity;
		force.normalize();
		force.mult(-pow(10, -10));
		applyForce(force);
	}

	void applyRepulsion(int i, float repRadius, float repStrength) {
		for (int j = 0; j < chain.nodes.size(); j++) {
			  if (i != j) {
				  float distance = PVector.sub(chain.nodes.get(i).location, chain.nodes.get(j).location).mag();
				  if ((distance > repRadius) && (distance < repRadius*4)) {
					  PVector force = chain.nodes.get(i).repulse(chain.nodes.get(j), repStrength);
					  chain.nodes.get(i).applyForce(force);
					  //stroke(255, 0, 255);
					  //line(nodes.get(i).location.x, nodes.get(i).location.y, nodes.get(j).location.x, nodes.get(j).location.y);
				  }
			  }
		  }
	}

	void applyForce(PVector force) {
		acceleration.add(force);
	}

	PVector repulse(Node m, float repStrength) {
		PVector force = PVector.sub(location, m.location);
		float distance = force.mag();
		distance = constrain(distance, 5.0, 20.0);
		force.normalize();
		float strength = (G*repStrength) / (distance * distance);
		force.mult(-strength);
		return force;
	}

	PVector attract(Node m, float attStrength) {
		PVector force = PVector.sub(location, m.location);
		float distance = force.mag();
		distance = constrain(distance, 5.0, 20.0);
		force.normalize();
		float strength = (G*attStrength) / (distance * distance);
		force.mult(strength);
		return force;
	}

	void boundaries() {
    	float d = 10;

    	if (location.x < d) {
      		acceleration.x *= -1;
   		}
    	else if (location.x > width -d) {
      		acceleration.x *= -1;
    	}

    	if (location.y < d) {
      		acceleration.y *= -1;
    	}
    	else if (location.y > height-d) {
      		acceleration.y *= -1;
    	}
  	}
}

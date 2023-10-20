import java.util.*;

public class Graph<V,E> {
    public class Vertex<V>{
        public V element;
        public HashMap<Vertex<V>,Edge<E>> outgoing, incoming;
        DoublyLinkedList.Node<Vertex<V>> position;

        public Vertex(V element, boolean graphIsDirected){
            this.element = element;
            outgoing = new HashMap<>();
            if(graphIsDirected)
                incoming = new HashMap<>();
            else
                incoming = outgoing;
        }
        public boolean validate(Graph<V,E> g){
            if(Graph.this == g) {
                return true;
            }
            else
                return false;
        }
    }
    public class Edge<E>{
        public E element;
        public E[] temp = (E[]) new Object[4];
        public Vertex<V>[] endpoints;
        DoublyLinkedList.Node<Edge<E>> position;

        public Edge(Vertex<V> u, Vertex<V> v, E element){
            this.element = element;
            endpoints = new Vertex[]{u,v};
        }
        public boolean validate(Graph<V,E> g){
            if(Graph.this == g) {
                return true;
            }
            else
                return false;
        }
    }
    private boolean isDirected;
    private DoublyLinkedList<Vertex<V>> vertices = new DoublyLinkedList<>();
    private DoublyLinkedList<Edge<E>> edges = new DoublyLinkedList<>();
    public Graph(boolean isDirected){this.isDirected = isDirected;}
    public int numVertices() {return vertices.size;}
    public int numEdges() {return edges.size;}
    public int outDegree(Vertex<V> v){ // put into the place where 'degree' is introduced.
        return v.outgoing.size();
    }
    public int inDegree(Vertex<V> v){
        return v.incoming.size();
    }

    public Vertex<V> opposite(Vertex<V> v, Edge<E> e){

        if(e.endpoints[0]==v) return e.endpoints[1];
        else if(e.endpoints[1]==v) return e.endpoints[0];
        else throw new IllegalArgumentException("the given vertex and edge do not match");
    }
    public Edge<E> getEdge(Vertex<V> u, Vertex<V> v){
        return u.outgoing.get(v);
    }

    public Vertex<V> insertVertex(V element){
        Vertex<V> newVertex = new Vertex(element, isDirected);
        vertices.addLast(newVertex);
        return newVertex;
    }
    public Edge<E> insertEdge(Vertex<V> u, Vertex<V> v, E element){
        Edge<E> newEdge = new Edge<>(u, v, element);
        u.outgoing.put(v,newEdge);
        v.incoming.put(u,newEdge);
        newEdge.position=edges.addLast(newEdge);
        return newEdge;
    }

    public void removeEdge(Edge<E> e){
        Vertex<V> origin = e.endpoints[0];
        Vertex<V> dest = e.endpoints[1];
        origin.outgoing.remove(dest);
        dest.incoming.remove(origin);
        edges.delete(e.position);
    }
    public void removeVertex(Vertex<V> v){
        // outgoing
        for (Edge<E> e: v.outgoing.values()){
            removeEdge(e);
        }
        // incoming
        for (Edge<E> e: v.incoming.values()){
            removeEdge(e);
        }
        // vertex list
        vertices.delete(v.position);
    }

    public HashMap<Vertex<V>,Edge<E>> DFSWrapper(Vertex<V> v){
        HashMap<Vertex<V>,Edge<E>> record = new HashMap<>();
        record.put(v,null);
        DFS(record,v);
        return record;
    }
    public void DFS(HashMap<Vertex<V>,Edge<E>> record, Vertex<V> u){
        for (Edge<E> e: u.outgoing.values()){
            Vertex<V> v = opposite(u, e);
            if(record.containsKey(v)==false){
                record.put(v,e);
                DFS(record,v);
            }
        }
    }

    public HashMap<Vertex<V>,Edge<E>> CycleDetectionWrapper(Vertex<V> v){
        HashMap<Vertex<V>,Edge<E>> record = new HashMap<>();
        HashMap<Vertex<V>,Edge<E>> ancestors = new HashMap<>();
        record.put(v,null);
        ancestors.put(v,null);
        CycleDetection(record,v,ancestors);
        return record;
    }
    public boolean CycleDetection(HashMap<Vertex<V>,Edge<E>> record, Vertex<V> u, HashMap<Vertex<V>,Edge<E>> ancestors){
        for (Edge<E> e: u.outgoing.values()){
            Vertex<V> v = opposite(u, e);
            if(ancestors.containsKey(v)) return true;
            if(record.containsKey(v)==false){
                record.put(v,e);
                ancestors.put(v,null);
                if (CycleDetection(record,v,ancestors)==true) return true;
                ancestors.remove(v);
            }
        }
        return false;
    }

    public ArrayList<Vertex<V>> topologicalSort(){
        ArrayList<Vertex<V>> ordering = new ArrayList<>();
        HashMap<Vertex<V>,Integer> inDegree = new HashMap<>();
        // Step 1: Find source initial vertices
        for (Vertex<V> v:vertices){
            inDegree.put(v,v.incoming.size());
            if(inDegree.get(v)==0){
                ordering.add(v);
            }
        }
        // Step 2: Prune DAG
        for(int i=0;i<ordering.size();i++){
            Vertex<V> curV = ordering.get(i);
            for (Vertex<V> v: curV.outgoing.keySet()){
                int newInDegree = inDegree.get(v)-1;
                inDegree.put(v,newInDegree);
                if(newInDegree == 0) ordering.add(v);
            }
        }
        return ordering;
    }



    public void printTopologicalOrdering(ArrayList<Vertex<V>> ordering){
        for(Vertex<V> v:ordering){
            //System.out.print("here");
            System.out.print(v.element);
        }
    }


    public HashMap<Vertex<V>,Edge<E>> BFS(Vertex<V> u){
        HashMap<Vertex<V>,Edge<E>> record = new HashMap<>();
        record.put(u,null);
        ArrayList<Vertex<V>> curLevel = new ArrayList<>();
        curLevel.add(u);
        while(!curLevel.isEmpty()){
            ArrayList<Vertex<V>> newLevel = new ArrayList<>();
            for(Vertex<V> x:curLevel){
                for(Vertex<V> v:x.outgoing.keySet()){
                    if(!record.containsKey(v)){
                        record.put(v,x.outgoing.get(v));
                        newLevel.add(v);
                    }
                }
            }
            curLevel = newLevel;
        }
        return record;
    }




}


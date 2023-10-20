import java.util.*;

public class HeapPriorityQueue<K,V>{

    protected static class Entry<K,V>{
        public K k;
        public V v;
        public Entry(K key, V value){
            k = key;
            v = value;
        }
    }

    protected ArrayList<Entry<K,V>> heap = new ArrayList<>();

    protected Comparator<K> comp;
    public HeapPriorityQueue(){this(new DefaultComparator<K>());}
    public HeapPriorityQueue(Comparator<K> c) {comp=c;}
    protected int leftchild(int j) {return 2*j+1;}
    protected int rightchild(int j) {return 2*j+2;}
    protected int parent(int j) {return (j-1)/2;}
    protected boolean hasLeft(int j) {return leftchild(j)<heap.size();}
    protected boolean hasRight(int j) {return rightchild(j)<heap.size();}
    protected void swap(int i, int j){
        Entry<K,V> temp = heap.get(i);
        heap.set(i,heap.get(j));
        heap.set(j,temp);
    }
    public int size(){
        return heap.size();
    }
    public boolean isEmpty(){
        return heap.size()==0;
    }
    public Entry<K,V> insert(K key, V value) {
        // FILL ME IN!
        Entry<K,V> newEntry = new Entry<>(key,value);
        heap.add(newEntry);
        swim(heap.size()-1);
        return newEntry;
    }



    public void swim(int j){
        // FILL ME IN!
        while(j>0){
            // compare key of current node against its pareant's
            if(comp.compare(heap.get(j).k,heap.get(parent(j)).k)<0){
                swap(j,parent(j));
                j=parent(j);
            }
            else{
                break;
            }
        }


    }

    public Entry<K,V> removeMin() {
        // FILL ME IN!
        if(size()==0) return null;
        swap(0,heap.size()-1);
        Entry<K,V> removed = heap.remove(heap.size()-1);
        sink(0);
        return removed;
    }
    public void sink(int j) {
        // FILL ME IN!
        while(hasLeft(j)){
            int minchild = leftchild(j);
            if(hasRight(j))
            {if(comp.compare(heap.get(minchild).k, heap.get(rightchild(j)).k)>0){
                minchild = rightchild(j);
            }}
            if(comp.compare(heap.get(j).k,heap.get(minchild).k)>0){
                swap(j,minchild);
                j=minchild;
            }
            else{
                break;
            }
        }

    }


    public Entry<K,V> min(){
        if(heap.size()==0) return null;
        return heap.get(0);
    }
    public void print(){
        for (Entry<K,V> e: heap){
            System.out.println(e.k);
        }
    }
}

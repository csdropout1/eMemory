import java.util.*;
public class HeapAdaptablePriorityQueue<K,V> extends HeapPriorityQueue<K,V> {
    protected static class AdaptableEntry<K,V> extends Entry<K,V>{
        private int index;
        public AdaptableEntry(K key, V value, int j){
            super(key,value);
            index = j;
        }
        public int getIndex(){return index;}
        public void setIndex(int j){index = j;}
    }
    public HeapAdaptablePriorityQueue(Comparator<K> c) {super(c);}
    public HeapAdaptablePriorityQueue(){super();}
    public AdaptableEntry<K,V> insert(K key, V value){
        AdaptableEntry<K,V> newEntry = new AdaptableEntry<>(key,value,heap.size());
        heap.add(newEntry);
        swim(heap.size()-1);
        return newEntry;
    }
    protected AdaptableEntry<K,V> validate(AdaptableEntry<K,V> entry) {
        if(entry.getIndex()<0||entry.getIndex()>=heap.size()||heap.get(entry.getIndex()).k != entry.k || heap.get(entry.getIndex()).v != entry.v){
            throw new IllegalArgumentException("Invalid Entry");
        }
        return entry;
    }
    public void remove(AdaptableEntry<K,V> entry){
        AdaptableEntry<K,V> toberemoved = validate(entry);
        int curLoc = toberemoved.getIndex();
        swap(curLoc,heap.size()-1);
        heap.remove(heap.size()-1);
        bubble(curLoc);
    }
    public void bubble(int j){
        if(comp.compare(heap.get(j).k,heap.get(parent(j)).k)<0){
            swim(j);
        }
        else{
            sink(j);
        }
    }
    //@Override
    protected void swap(int i, int j){
        super.swap(i,j);
        ((AdaptableEntry<K,V>) heap.get(i)).setIndex(i);
        ((AdaptableEntry<K,V>) heap.get(j)).setIndex(j);
    }
    public void replaceKey(AdaptableEntry<K,V> entry, K key){
        int curIndex = entry.getIndex();
        heap.get(curIndex).k = key;
        bubble(curIndex);
    }
    public AdaptableEntry<K,V> removeMin(){
        swap(0,heap.size()-1);
        AdaptableEntry<K,V> toberemoved = (AdaptableEntry<K,V>) heap.remove(heap.size()-1);
        sink(0);
        return toberemoved;
    }

    public void replaceValue(AdaptableEntry<K,V> entry, V value){
        AdaptableEntry<K,V> locator = validate(entry);
        heap.get(locator.index).v=value;
    }

    public AdaptableEntry<K,V> min(){
        if(heap.size()==0) return null;
        return (AdaptableEntry<K,V>)heap.get(0);
    }
}


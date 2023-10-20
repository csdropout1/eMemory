public class LinkedListQueue<E> implements Queue<E>{
    private SinglyLinkedList<E> ll = new SinglyLinkedList();
    /** Returns the number of elements in the queue. */
    public int size(){return ll.size();};
    /** Tests whether the queue is empty. */
    public boolean isEmpty( ){return(size()==0);};
    /** Inserts an element at the rear of the queue. */
    public void enqueue(E e){ll.addLast(e);};
    /** Returns, but does not remove, the first element of the queue (null if empty). */
    public E first( ){return ll.first();};
    /** Removes and returns the first element of the queue (null if empty). */
    public E dequeue( ){return ll.removeFirst();};
}

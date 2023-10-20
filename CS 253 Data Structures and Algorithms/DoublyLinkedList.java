import java.util.*;
public class DoublyLinkedList<E> implements Iterable<E>{
    public static class Node<E>{
        public E element;
        public Node<E> previous;
        public Node<E> next;
        public Node(E e,Node<E> p,Node<E> n){
            element = e;
            previous = p;
            next = n;
        }
    }
    public Node<E> head;
    public Node<E> tail;
    public int size=0;
    public DoublyLinkedList(){
        head = new Node<E>(null,null,null);
        tail = new Node<E>(null,head,null);
        head.next = tail;
    }
    public E delete(Node<E> n){
        Node<E> previous = n.previous;
        Node<E> next = n.next;
        previous.next = next;
        next.previous = previous;
        size--;
        return n.element;
    }
    public Node<E> insert(E e, Node<E> previous, Node<E> next){
        Node<E> current = new Node<E>(e,previous,next);
        previous.next = current;
        next.previous = current;
        size++;
        return current;
    }
    public void print(){
        Node<E> curNode = head.next;
        while(curNode.element != null){
            System.out.print(curNode.element);
            curNode = curNode.next;
        }
    }
    public Node<E> addLast(E e){
        Node<E> current = insert(e,tail.previous,tail);
        return current;
    }
    private class PositionIterator implements Iterator<Node<E>>{
        private Node<E> cursor = head.next;
        private Node<E> recent = null;
        public boolean hasNext() {return (cursor.next != null);}
        public Node<E> next() throws NoSuchElementException {
            if (cursor == null) throw new NoSuchElementException("nothing left");
            recent = cursor;
            cursor = cursor.next;
            return recent;
        }
        public void remove() throws IllegalStateException {
            if (recent == null) throw new IllegalStateException("nothing to remove");
            DoublyLinkedList.this.delete(recent);
            recent = null;
        }
    }
    private class PositionIterable implements Iterable<Node<E>>{
        public Iterator<Node<E>> iterator() {return new PositionIterator();}
    }
    public Iterable<Node<E>> positions(){
        return new PositionIterable();
    }
    private class ElementIterator implements Iterator<E> {
        Iterator<Node<E>> posIterator = new PositionIterator();
        public boolean hasNext() {return posIterator.hasNext();}
        public E next() {return posIterator.next().element;}
        public void remove() {posIterator.remove();}
    }
    public Iterator<E> iterator() {return new ElementIterator();}
}


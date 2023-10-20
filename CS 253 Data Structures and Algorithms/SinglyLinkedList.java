public class SinglyLinkedList<E>{
    private static class Node<E>{
        private E element;
        private Node<E> next;
        public Node(E e, Node<E> n){
            element = e;
            next = n;
        }
        public E getElement(){
            return element;
        }
        public Node<E> getNext(){
            return next;
        }
        public void setNext(Node<E> n){
            next = n;
        }
    }
    private Node<E> head = null;
    private Node<E> tail = null;
    private int size = 0;
    public int size(){return size;}
    public E first(){
        if(size==0){return null;}
        return head.element;
    }
    public SinglyLinkedList(){}
    public void addLast(E e){
        Node<E> cur_node = new Node<E>(e,null);
        if(size()==0){head=cur_node;}
        else{tail.next=cur_node;}
        tail = cur_node;
        size++;
    }
    public E removeFirst(){
        if(size()==0) return null;
        E answer = head.element;
        head = head.next;
        size--;
        if(size()==0) tail=null;
        return answer;
    }
}